from typing import Dict, Any, List
import json
import re

# ✅ Prefer new package if available, else fallback
try:
    from langchain_ollama import ChatOllama
except Exception:
    from langchain_community.chat_models import ChatOllama

from app.utils.config import settings
from app.tools.financial_extractor import extract_financial_metrics
from app.tools.qualitative_rag import QualitativeAnalysisTool
from app.tools.market_data import fetch_tcs_stock_price
from app.utils.logger import get_logger

log = get_logger("ForecastAgent")


# ✅ IMPORTANT: keep schema braces normal here (NO formatting will run on this)
SYSTEM_PROMPT = """
You are ForecastGPT, a financial forecasting agent for Tata Consultancy Services (TCS).

Rules:
- Use ONLY provided financial metrics and transcript evidence.
- If evidence is missing or unclear, say so explicitly in the JSON.
- Output ONLY valid JSON matching the schema.
- Do not add any extra keys outside schema.

Schema (follow EXACT structure):

{
  "company": "TCS",
  "period_analyzed": ["string"],
  "financial_trends": {
     "revenue": "string",
     "net_profit": "string",
     "operating_margin": "string"
  },
  "management_themes": ["string"],
  "risks": ["string"],
  "opportunities": ["string"],
  "qualitative_forecast_next_quarter": "string",
  "confidence": {
     "level": "low|medium|high",
     "reasons": ["string"]
  },
  "sources": {
     "financial_docs": ["string"],
     "transcripts": ["string"]
  },
  "market_context": {}
}
"""


def _safe_json_extract(text: str) -> Dict[str, Any]:
    """
    Robust JSON extraction:
    - Direct JSON
    - JSON inside markdown
    - Extra text around JSON
    """
    text = text.strip()

    # 1) direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2) find first {...} block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        json_str = match.group(0)
        return json.loads(json_str)

    raise ValueError("No valid JSON found in model output")


class ForecastAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model=getattr(settings, "OPENAI_MODEL", "llama3.2"),
            temperature=0.2
        )

    def run(self, query: str, financial_pdfs: List[str], transcripts: List[str]) -> Dict[str, Any]:
        # ✅ 1. Extract financial metrics
        fin = extract_financial_metrics(financial_pdfs)

        # ✅ 2. Transcript RAG safely
        themes = []
        try:
            if transcripts:
                rag = QualitativeAnalysisTool()
                rag.build_index(transcripts)
                themes = rag.query_themes([
                    "revenue growth drivers and headwinds",
                    "margin outlook and cost pressures",
                    "deal pipeline and demand commentary",
                    "AI/GenAI and cloud opportunities",
                    "key risks mentioned by management"
                ])
            else:
                themes = ["No transcript provided by user."]
        except Exception as e:
            log.warning(f"Transcript RAG failed: {e}")
            themes = ["Transcript analysis failed due to indexing error."]

        # ✅ 3. Market data safe fallback (429 won't break run)
        try:
            market = fetch_tcs_stock_price()
        except Exception as e:
            log.warning(f"Market fetch failed, continuing without it: {e}")
            market = {}

        # ✅ 4. MANUAL user prompt (NO ChatPromptTemplate formatting)
        user_prompt = f"""
Task: {query}

Financial metrics extracted from quarterly documents:
{fin}

Semantically retrieved transcript evidence:
{themes}

Optional market context (may be empty):
{market}

Return ONLY the forecast JSON now.
"""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        res = self.llm.invoke(messages).content

        # ✅ 5. Parse strict JSON
        try:
            parsed = _safe_json_extract(res)

            # Ensure required top-level keys always exist
            parsed.setdefault("company", "TCS")
            parsed.setdefault("period_analyzed", [])
            parsed.setdefault("financial_trends", {
                "revenue": "unclear",
                "net_profit": "unclear",
                "operating_margin": "unclear"
            })
            parsed.setdefault("management_themes", [])
            parsed.setdefault("risks", [])
            parsed.setdefault("opportunities", [])
            parsed.setdefault("qualitative_forecast_next_quarter", "")
            parsed.setdefault("confidence", {
                "level": "low",
                "reasons": ["Missing confidence from model"]
            })
            parsed.setdefault("sources", {
                "financial_docs": financial_pdfs,
                "transcripts": transcripts
            })
            parsed.setdefault("market_context", market)

            return parsed

        except Exception as e:
            log.error(f"Model returned invalid JSON: {e}")

            return {
                "company": "TCS",
                "period_analyzed": [],
                "financial_trends": {
                    "revenue": "unclear",
                    "net_profit": "unclear",
                    "operating_margin": "unclear"
                },
                "management_themes": themes if themes else [],
                "risks": ["Model output invalid JSON"],
                "opportunities": [],
                "qualitative_forecast_next_quarter": "",
                "confidence": {
                    "level": "low",
                    "reasons": ["Invalid JSON from model"]
                },
                "sources": {
                    "financial_docs": financial_pdfs,
                    "transcripts": transcripts
                },
                "market_context": market
            }

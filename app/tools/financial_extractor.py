import re
from typing import Dict, Any, List, Optional
import pdfplumber
from app.utils.text import clean_text
from app.utils.logger import get_logger

log = get_logger("FinancialDataExtractorTool")

def _extract_text_from_pdf(path: str) -> str:
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    return clean_text("\n".join(texts))

def _find(patterns: List[str], text: str) -> Optional[str]:
    for pat in patterns:
        m = re.search(pat, text, flags=re.I)
        if m:
            return m.group(1)
    return None

def extract_financial_metrics(pdf_paths: List[str]) -> Dict[str, Any]:
    """Extract key metrics from quarterly financial PDFs."""
    docs = []
    for p in pdf_paths:
        try:
            text = _extract_text_from_pdf(p)
        except Exception as e:
            log.error(f"PDF read failed {p}: {e}")
            continue

        metrics = {}
        metrics["total_revenue_inr_cr"] = _find([
            r"total\s+revenue[^₹]{0,20}₹\s*([\d,]+\.?\d*)\s*crore",
            r"revenue[^₹]{0,20}₹\s*([\d,]+\.?\d*)\s*crore",
        ], text)

        metrics["net_profit_inr_cr"] = _find([
            r"net\s+profit[^₹]{0,20}₹\s*([\d,]+\.?\d*)\s*crore",
            r"profit\s+after\s+tax[^₹]{0,20}₹\s*([\d,]+\.?\d*)\s*crore",
        ], text)

        metrics["operating_margin_pct"] = _find([
            r"operating\s+margin[^\d]{0,10}([\d.]+)\s*%",
            r"ebit\s+margin[^\d]{0,10}([\d.]+)\s*%",
        ], text)

        docs.append({"path": p, "metrics": metrics})

    trend = {"docs_analyzed": [d["path"] for d in docs]}
    if len(docs) >= 2:
        trend["revenue_direction"] = "compare latest vs previous"
        trend["margin_direction"] = "compare latest vs previous"

    return {"documents": docs, "trend_summary": trend}

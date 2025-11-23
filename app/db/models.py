from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, JSON, String, Text
from sqlalchemy.sql import func

Base = declarative_base()

class ForecastLog(Base):
    __tablename__ = "forecast_logs"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    input_meta = Column(JSON, nullable=True)
    output_json = Column(JSON, nullable=False)
    model_used = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

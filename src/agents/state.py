from typing import TypedDict


class AgentState(TypedDict):
    ticker: str
    last_close: float
    rsi14: float
    forecast: list
    performance_analysis: str
    news_sentiment: str
    final_report: str
    recommendation: str

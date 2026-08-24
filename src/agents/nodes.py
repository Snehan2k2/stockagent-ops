import re

from langchain_core.messages import SystemMessage

from src.agents.llm import llm
from src.agents.state import AgentState


def performance_analyst_node(state: AgentState) -> dict:
    prompt = f"""You are a quantitative analyst. Analyze this forecast for {state['ticker']}:

Last close: {state['last_close']}
RSI14: {state['rsi14']}
5-day forecast: {state['forecast']}

In 2-3 concise sentences, describe the trend direction and what the RSI suggests about momentum.
"""
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"performance_analysis": response.content}


def market_expert_node(state: AgentState) -> dict:
    import yfinance as yf

    try:
        news_items = yf.Ticker(state["ticker"]).news[:5]
        headlines = [
            item["content"]["title"]
            for item in news_items
            if item.get("content", {}).get("title")
        ]
    except Exception:
        headlines = []

    news_text = "\n".join(f"- {h}" for h in headlines) if headlines else "No recent news available."

    prompt = f"""You are a market strategist. Recent headlines for {state['ticker']}:

{news_text}

In 2-3 concise sentences, summarize overall sentiment and any notable catalysts or risks.
"""
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"news_sentiment": response.content}


def report_generator_node(state: AgentState) -> dict:
    prompt = f"""Write a concise markdown stock report for {state['ticker']}.

TECHNICAL ANALYSIS:
{state['performance_analysis']}

MARKET SENTIMENT:
{state['news_sentiment']}

Structure:
# {state['ticker']} Analysis Report

## Technical Outlook
[2-3 sentences]

## Market Sentiment
[2-3 sentences]

## Recommendation
**Stance:** BULLISH/BEARISH/NEUTRAL
**Rationale:** [1 sentence]
"""
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"final_report": response.content}


def _extract_stance(text: str) -> str:
    match = re.search(r"\*\*Stance:\*\*\s*(BULLISH|BEARISH|NEUTRAL)", text, re.IGNORECASE)
    return match.group(1).upper() if match else "NEUTRAL"


def critic_node(state: AgentState) -> dict:
    prompt = f"""You are a senior editor reviewing this financial report for {state['ticker']}:

{state['final_report']}

Check it aligns with this data:
- Technical: {state['performance_analysis']}
- Sentiment: {state['news_sentiment']}

Output the final, polished report (fix only real issues; return unchanged if it's already good).
Keep the "## Recommendation" section's structure exactly as-is, including the literal
"**Stance:** BULLISH/BEARISH/NEUTRAL" line — you may revise the rationale, but do not
reformat or relabel the Stance line itself.
"""
    response = llm.invoke([SystemMessage(content=prompt)])
    text = response.content
    return {"final_report": text, "recommendation": _extract_stance(text)}

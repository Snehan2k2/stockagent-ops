import requests
import streamlit as st

st.set_page_config(page_title="Stock Agent Ops", layout="centered")
st.title("📈 Stock Analysis")

ticker = st.text_input("Ticker", value="AAPL").upper().strip()
question = st.text_input("Question (optional)", placeholder="e.g. should I buy this right now?")

if st.button("Analyze"):
    if not ticker:
        st.error("Enter a ticker.")
    else:
        with st.spinner("Analyzing..."):
            params = {"question": question} if question else {}
            try:
                #resp = requests.get(f"http://127.0.0.1:8000/analyze/{ticker}", params=params, timeout=60)
                resp = requests.get(f"http://backend:8000/analyze/{ticker}", params=params, timeout=60)
                resp.raise_for_status()
                data = resp.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
                data = None

        if data:
            st.subheader(f"{data['ticker']} — {data['recommendation']}")
            st.metric("Last Close", f"${data['last_close']:.2f}")
            st.line_chart(data["forecast"])
            st.markdown(data["report"])
            st.caption(f"cache: {data.get('cache_type', data.get('cached'))}")
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3.5:2b", reasoning=False, temperature=0.3)

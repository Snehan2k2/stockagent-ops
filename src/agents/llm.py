from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3.5:2b", reasoning=False, temperature=0.3, base_url="http://host.docker.internal:11434")

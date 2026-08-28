FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-install-project
COPY . .
EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "frontend/app.py", "--server.address", "0.0.0.0"]
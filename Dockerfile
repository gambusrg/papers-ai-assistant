FROM python:3.12.13-slim-bookworm
WORKDIR /app

COPY pyproject.toml uv.lock .

RUN pip install uv
RUN  uv sync --frozen
RUN uv run python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY . .

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "src.adapters.input.rest.api:app", "--host", "0.0.0.0", "--port", "8080"]



FROM python:3.14
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

COPY . .
RUN uv sync --frozen --no-cache

COPY ./app ./app
COPY ./public ./public

CMD ["uv","run","uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]

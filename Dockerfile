FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src /src

WORKDIR /src

ENV PATH="/.venv/bin:$PATH"

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]

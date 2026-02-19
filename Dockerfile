FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src /src

WORKDIR /src

ENV PATH="/.venv/bin:$PATH"

RUN python manage.py collectstatic --noinput

ENV DJANGO_DEBUG_FALSE=1
RUN adduser --uid 1234 nonroot --disabled-password --gecos "" && chown -R nonroot:nonroot /src
USER nonroot

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]

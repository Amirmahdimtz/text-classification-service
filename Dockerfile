FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ENV_TYPE=production
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && groupadd --system app && useradd --system --gid app app
COPY src ./src
USER app
EXPOSE 8000
CMD ["uvicorn", "src.host.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml README.md requirements.lock.txt ./
COPY cad_api ./cad_api
RUN pip install --no-cache-dir -r requirements.lock.txt
RUN pip install --no-cache-dir --no-deps .
ENV CAD_DATA_DIR=/data PYTHONUNBUFFERED=1
VOLUME ["/data"]
EXPOSE 8080
CMD ["uvicorn", "cad_api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]

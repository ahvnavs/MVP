FROM python:3.12-slim

WORKDIR /app

COPY infra/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/virtual_smart_meter.py .

EXPOSE 8080

CMD ["python", "virtual_smart_meter.py"]

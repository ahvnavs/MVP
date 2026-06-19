FROM python:3.12-slim

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY virtual_smart_meter.py .

EXPOSE 8080

CMD [ "python", "virtual_smart_meter.py" ]

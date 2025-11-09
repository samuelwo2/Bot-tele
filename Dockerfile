FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m botuser && chown -R botuser /app
USER botuser

EXPOSE 8000

CMD ["python", "multi_bot.py"]
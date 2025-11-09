# Dockerfile for running multi_bot.py
FROM python:3.11-slim

# Tránh buffer output (log realtime)
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

WORKDIR /app

# Copy and install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# (Tuỳ ý) tạo user không root (an toàn hơn)
RUN useradd -m botuser && chown -R botuser /app
USER botuser

# Command to run the bot
# Nếu file chính của bạn là multi_bot.py thì giữ nguyên; đổi nếu khác.
CMD ["python", "multi_bot.py"]
FROM python:3.10-slim-buster

WORKDIR /app

COPY pyproject.toml .
COPY imagenet_classes.txt .
COPY src /app/src
RUN pip install --no-cache-dir .

EXPOSE 5000

# デモなのでFlaskに内蔵されているサーバーを使う
CMD ["flask", "--app", "pictag", "run", "--host=0.0.0.0"]

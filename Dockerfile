# Create python 3.10 contaienr
FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt .
COPY . .

RUN apt update && apt upgrade -y
RUN pip install -r requirements.txt

CMD ["python", "-m", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# Create python 3.10 contaienr
FROM python:3.10-slim-buster as python
WORKDIR /app
COPY requirements.txt .
COPY . .

RUN apt update && apt upgrade -y
RUN pip install -r requirements.txt

# Run python 3.10 container
FROM python:3.10-slim-buster as python-run
WORKDIR /app
COPY --from=python /app .
CMD ["poetry", "run", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

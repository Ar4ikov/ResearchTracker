# Create python 3.10 contaienr
FROM python:3.10-alpine3.14 as python
WORKDIR /app
COPY ./src/backend/requirements.txt ./

RUN sudo apt update && sudo apt upgrade -y
RUN pip install -r requirements.txt

# Run python 3.10 container
FROM python:3.10-alpine3.14 as python-run
WORKDIR /app
COPY --from=python /app ./
CMD ["python", "app.py"]

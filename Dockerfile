FROM python:3.10

WORKDIR /masks

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py server run"]

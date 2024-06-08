FROM python:3.11-buster

# Print Python path
RUN python -c "import sys; print(sys.path)"

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD gunicorn --bind 0.0.0.0:8000 --workers 3 stock_predictor.wsgi:application

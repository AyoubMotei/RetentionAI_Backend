FROM python:3.11

WORKDIR /app

COPY  requirements.txt .

RUN apt-get update && apt-get install -y build-essential pkg-config libfreetype-dev libpng-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
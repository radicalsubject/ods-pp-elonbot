FROM python:3.8-slim
# Install manually all the missing libraries
RUN apt-get update -qq && apt-get install -y tesseract-ocr
# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/bot.py
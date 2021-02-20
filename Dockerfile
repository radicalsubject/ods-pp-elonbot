# FROM python:3.8-slim
# # Install manually all the missing libraries
# RUN apt-get update -qq && apt-get install -y tesseract-ocr
# # Install Python dependencies.
# RUN apt update && apt install -y libsm6 libxext6
# COPY requirements.txt requirements.txt
# RUN apt-get -y install tesseract-ocr
# RUN apt-get update
# RUN apt-get -y install libleptonica-dev 
# RUN apt-get -y install tesseract-ocr tesseract-ocr-dev
# RUN apt-get -y install libtesseract-dev
# RUN pip install -r requirements.txt
# RUN pip install pillow
# RUN pip install pytesseract 

# RUN mkdir /app
# ADD . /app
# WORKDIR /app

# CMD python /app/bot.py
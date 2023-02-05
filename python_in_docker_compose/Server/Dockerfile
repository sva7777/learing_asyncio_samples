FROM python:3.8-alpine
RUN apk update
RUN mkdir /app
ADD main.py /app
ADD  requirements.txt /app
WORKDIR /app

RUN pip3 install -r requirements.txt
CMD ["python3","main.py"]



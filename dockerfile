FROM python:3.8-alpine
 
WORKDIR .
 
EXPOSE 8080
 
RUN apk update && apk add --virtual build-dependencies \
   python3-dev gcc build-base
 
COPY requirements.txt .
 
RUN pip install -r requirements.txt -vvv && apk del build-dependencies

CMD python main.py

COPY . .


 

 
 
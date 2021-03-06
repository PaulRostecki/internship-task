FROM alpine:latest

RUN apk update && \
    apk add python3 py3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]

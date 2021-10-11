# base image
FROM alpine:latest
# Run - install. APK - Alpine Package Manager
RUN apk add --no-cache python3-dev \
    && apk add py3-pip \
    && pip install --upgrade pip
WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt                                                                            

EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["app.py"]


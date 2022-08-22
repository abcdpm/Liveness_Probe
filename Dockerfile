FROM python:3.8-alpine

RUN mkdir /appl && \
    apk add --no-cache bash git busybox-extras tzdata vim && \
    git clone https://github.com/abcdpm/Liveness_Probe.git "/appl" && \
    pip install -r ./Liveness_Probe/requirements.txt && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone && \
    apk del tzdata

WORKDIR /appl

CMD ["python3", "/Liveness_Probe/main.py"]
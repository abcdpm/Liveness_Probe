FROM python:3.10-alpine

RUN mkdir /appl && \
    apk add --no-cache bash git busybox-extras tzdata vim && \
    git clone https://github.com/abcdpm/Liveness_Probe.git "/appl" && \
    pip install -r /appl/requirements.txt && \
    mkdir /appl/logs && \
    echo "Liveness_Probe Application Starts." >> /appl/logs/Liveness_Probe.log && \
    mkdir /appl/configs && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone && \
    apk del tzdata

WORKDIR /appl

CMD ["sh", "-c", "/appl/run.sh & tail -f /appl/logs/Liveness_Probe.log"]
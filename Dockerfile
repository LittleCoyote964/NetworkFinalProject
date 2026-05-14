FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    strace \
    tcpdump \
    iproute2 \
    net-tools \
    procps \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /sandbox

COPY . /sandbox

RUN mkdir -p \
    /sandbox/logs \
    /sandbox/report \
    /sandbox/sandbox_area

CMD ["/bin/bash"]
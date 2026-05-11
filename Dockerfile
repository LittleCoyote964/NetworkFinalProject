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

CMD ["/bin/bash"]
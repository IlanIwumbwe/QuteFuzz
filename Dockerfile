FROM ubuntu:23.10

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

WORKDIR /qutefuzz

COPY . .
    
RUN python3 -m venv .qutefuzz

RUN /bin/bash -c "source .qutefuzz/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

RUN chmod +x ./run.sh


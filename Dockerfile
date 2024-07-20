FROM pytorch/torchserve:latest

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

COPY . .

USER root 
RUN chmod +x entrypoint.sh

ENTRYPOINT ./entrypoint.sh


FROM pytorch/torchserve:latest

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["torchserve", "--start", "--model-store", "app/model_store", "--models", "bert_content_processing.mar", "--ts-config", "app/config.properties", "--foreground"]


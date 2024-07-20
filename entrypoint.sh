#!/bin/bash

python download_model.py

torchserve --start --model-store app/model_store --models bert_content_processing.mar --ts-config app/config.properties --foreground
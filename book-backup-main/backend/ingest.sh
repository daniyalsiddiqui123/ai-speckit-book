#!/bin/bash
# Set environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found. Please create one based on .env.example"
  exit 1
fi

python -m data_ingestion.ingest

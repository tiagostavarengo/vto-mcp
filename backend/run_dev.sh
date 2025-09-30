#!/bin/bash
# Script to run the FastAPI development server

echo "Starting FastAPI server with auto-reload..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

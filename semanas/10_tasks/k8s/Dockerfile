FROM python:3.11-slim
RUN pip install --no-cache-dir kubernetes
COPY scan_images.py /app/scan_images.py
RUN chmod +x /app/scan_images.py
WORKDIR /app
CMD ["python3", "scan_images.py"]

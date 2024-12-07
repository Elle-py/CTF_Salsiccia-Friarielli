FROM python:3.9-slim
WORKDIR ~/Desktop/ctf
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY flag.txt flag.txt
COPY templates/ templates/
COPY static/ static/
COPY secrets/ secrets/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]

FROM python:3.8-slim-buster

EXPOSE 8080
WORKDIR app
RUN useradd -u 1001 -m app 
RUN chown app:app -R .
RUN \
    apt-get update && \
    apt-get install make
USER app 
ENV PATH /home/app/.local/bin:$PATH
COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY . .
RUN make clients
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

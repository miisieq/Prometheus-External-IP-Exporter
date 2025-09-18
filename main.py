#!/usr/bin/python3
# pylint: disable=C0116
"""
Simple Prometheus exporter returning external IP v4 address.
"""
import ipaddress
from fastapi import FastAPI, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest
import requests
import uvicorn

app = FastAPI()
registry = CollectorRegistry()

metric = Gauge(
    "external_ip",
    "Current external IP address",
    ["ip"],
    registry=registry,
)

@app.get("/")
async def get_index():
    content = """
    <html>
        <head><title>Prometheus External IP Exporter</title></head>
        <body>
            <h1>Prometheus External IP Exporter</h1>
            <p><a href="metrics">Metrics</a></p>
            <p><a href="health">Healtcheck</a></p>
        </body>
    </html>
    """

    return Response(
        content=content,
        media_type="text/html; charset=utf-8"
    )

@app.get("/health")
async def get_health():
    return "I'm okay!"

@app.get("/metrics")
def metrics():
    response = requests.get("https://ifconfig.co/ip", timeout=5)
    content = response.text.strip()
    address = ipaddress.ip_address(content)
    metric.labels(ip=address).set(1)

    return Response(
        content=generate_latest(registry),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

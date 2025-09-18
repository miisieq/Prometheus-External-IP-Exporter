#

```bash
$ docker run --rm -p 8000:8000 miisieq/prometheus-external-ip-exporter:latest
```

```bash
$ curl localhost:8000/metrics
# HELP external_ip Current external IP address
# TYPE external_ip gauge
external_ip{ip="94.168.140.43"} 1.0
```
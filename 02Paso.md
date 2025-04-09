
## Instrumentacion

### Instalar la base para autoinstrumentar
```bash
pip install opentelemetry-distro
opentelemetry-bootstrap -a install
```


### Ejecutar la app instrumentada
```bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name lanzardado-server \
    flask run -p 8080
```

### Verificar la app
http://localhost:8080/lanzardado

### Lanzar por navegador o por curl
```bash
# Anonimo
curl -X GET http://localhost:8080/lanzardado
# Player uno
curl -X GET http://localhost:8080/lanzardado?jugador=uno
```


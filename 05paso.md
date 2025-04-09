
## Grafana

### Subir el grafana
```bash
ln -s $PWD/grafana /tmp/grafana
docker run -p 3000:3000 --rm --name grafana --network devops \
  -v /tmp/grafana/grafana.ini:/etc/grafana/grafana.ini \
  -v /tmp/grafana/provisioning/:/etc/grafana/provisioning/ \
  docker.io/grafana/grafana:11.5.2 
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

### Verificar en grafana
http://localhost:3000/grafana/

#### Query para prometheus
```json
{job="unknown_service"}
```

#### Query para jaeger
Seleccionar Search y en Service Name unknow_service
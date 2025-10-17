# Ruleta Rusa

Aplicación web que simula una ruleta rusa digital. El proyecto se divide en un servicio que carga el tambor del revólver y una interfaz web que permite al usuario “recargar” y “jalar el gatillo”. La comunicación entre ambos componentes se realiza a través de Redis.

## Arquitectura
- **Cliente (`client/`)**: Aplicación Flask que expone la interfaz web (`serv-client.py`) y consulta a Redis para obtener el tambor actual. Distribuye la plantilla HTML en `templates/index.html`.
- **Servidor (`server/`)**: Proceso Python que garantiza que siempre exista un tambor cargado en Redis (`server.py`). Cada tambor es una cadena de seis caracteres con un único `1` que representa la bala.
- **Redis**: Base de datos en memoria que actúa como intermediario entre cliente y servidor. La clave `rev` almacena el estado del tambor vigente.
- **Contenedores**: Cada componente cuenta con su `Dockerfile` basado en `python:3-alpine`. El archivo `docker-compose.yml` orquesta los servicios `server`, `client` y `redis-cluster`.
- **Manifests de Kubernetes**: Los archivos `client.yaml` y `server.yaml` contienen ejemplos de `Deployment`/`Service` para ejecutar las imágenes publicadas (`carlospmve/ruleta_rusa-*`) en un clúster.

## Requisitos
- Docker y Docker Compose para la ejecución con contenedores.
- Opcional: Python 3.9+ y Redis si se desea ejecutar los servicios directamente en el host.

## Puesta en marcha con Docker Compose
1. Clonar este repositorio y ubicarse en la raíz del proyecto.
2. Lanzar los servicios:
   ```bash
   docker-compose up
   ```
   *(Agregar `-d` si se prefiere correrlos en segundo plano).*
3. Abrir `http://localhost:5000` en el navegador. El botón **Recargar** solicita un nuevo tambor y **Jalar el gatillo** consume las posiciones de ese tambor hasta encontrar la bala.


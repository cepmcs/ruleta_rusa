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

El `docker-compose.yml` hace referencia a imágenes ya construidas y publicadas. Si se modifica el código y se desean imágenes locales, se puede reemplazar la sección `image` por instrucciones `build` apuntando a `client/` y `server/`, o generar nuevas imágenes y etiquetarlas con los mismos nombres.

## Ejecución local sin contenedores
1. Iniciar Redis accesible bajo el host `redis-cluster`. Algunas opciones:
   - Ejecutar `docker run --name redis-cluster -p 6379:6379 redis:alpine` y añadir `127.0.0.1 redis-cluster` al archivo `/etc/hosts`.
   - O bien, modificar temporalmente el host en `client/serv-client.py` y `server/server.py` para apuntar a `localhost`.
2. Crear y activar un entorno virtual en cada carpeta (`client/` y `server/`) e instalar dependencias:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Ejecutar los servicios en terminales separadas:
   ```bash
   # En server/
   python server.py

   # En client/
   python serv-client.py
   ```
4. Visitar `http://localhost:5000`.

## Endpoints expuestos
- `POST /recargar` (cliente): Obtiene el valor actual del tambor y lo elimina de Redis (`GETDEL`). Responde con una cadena de 6 caracteres (`0` = vacío, `1` = bala).
- `GET /` (cliente): Renderiza la interfaz HTML de juego.

## Despliegue en Kubernetes
- `client.yaml`: Incluye un `Deployment` y un `Service` tipo `LoadBalancer`. Ajustar los puertos según el entorno (la aplicación escucha en el puerto 5000).
- `server.yaml`: Define un `Deployment` para la imagen del servidor. Debe coexistir con una instancia accesible de Redis.

## Próximos pasos sugeridos
- Externalizar la configuración (host/puerto de Redis) mediante variables de entorno.
- Agregar pruebas automatizadas o validaciones para el flujo del tambor.
- Añadir un pipeline que construya y publique las imágenes del cliente y el servidor tras cada cambio.

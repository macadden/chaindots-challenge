# challenge-chaindots

Este es un proyecto basado en **Python**, **Django**, **Django REST Framework** y **PostgreSQL**.
Permite a los usuarios crear publicaciones, seguir a otros usuarios y comentar en publicaciones.

- NOTA: Este proyecto también fue realizado con Docker, pero debido a inconvenientes con la base de datos, decidí subirlo sin Docker.

## Requisitos

. Python 3.9
. PostgreSQL
. Poetry

## Instalación

### 1. Clonar el repositorio
```git clone [url_del_repositorio]```
```cd chaindots```

### 2. Instalar dependencias

Utilizá Poetry para gestionar las dependencias del proyecto. Si no tenés Poetry instalado, seguí las instrucciones en su documentación oficial.

.Chequeá tener **Python 3.9** instalado. Luego, ejecutá los siguientes comandos:

```poetry env use $(which python3)```
```poetry install```

Si es necesario, ejecutá:
```poetry install --no-root```
```poetry lock --no-update```

Ejecutá:
```poetry shell```

### 3. Configurar la base de datos y .env

- Chequeá de tener PostgreSQL instalado y configurado. Creá una base de datos para el proyecto y ajustá la configuración en el archivo settings.py.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_tu_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

- Por otro lado, no olvides crear un .env.

### 4. Aplicar migraciones

```python manage.py migrate```

### 5. Crear un superusuario

```python manage.py createsuperuser```

### 6. Iniciar el servidor

```python manage.py runserver```

## Uso de la API

- La API de Chaindots expone los siguientes endpoints:

### Usuarios

- ```GET /api/users/```: Recuperar una lista de todos los usuarios.
- ```GET /api/users/{id}/```: Recuperar detalles de un usuario específico.
- ```POST /api/users/```: Crear un nuevo usuario.
- ```POST /api/users/{id}/follow/{id}```: Seguir a otro usuario.

### Publicaciones

- ```GET /api/posts/```: Recuperar una lista de todas las publicaciones con filtros y paginación.
- ```GET /api/posts/{id}/```: Recuperar detalles de una publicación específica con los últimos tres comentarios.
- ```POST /api/posts/```: Crear una nueva publicación.

### Comentarios

- ```GET /api/posts/{id}/comments/```: Recuperar todos los comentarios para una publicación específica.
- ```POST /api/posts/{id}/comments/```: Agregar un nuevo comentario a una publicación.


- Gracias por la oportunidad :)
# API REST

Arquitectura de aplicaciones Web
API Rest
Unidad 2 - Actividad de entrega 1

Presentado por:
John Jairo Martínez Nieto

Profesor
Wilson Eduardo Soto Forero 

Institución Universitaria Politécnico Grancolombiano
Escuela de tecnologías de la información y las comunicaciones
Maestría en Arquitectura de Software
2025


Video: https://youtu.be/9tVkIGV9WRc
Repositorio: https://github.com/solucionesjj/apirest

## Objetivo General
* Desarrollar una API REST para facilitar el intercambio de información de forma segura

## Especificaciones
* **Especificaciones técnicas**
	* La API se debe desarrollar usando Python y FastAPI
	* La API debe tener documentación usando OpenAPI (Swagger)
	* Utilizar SQLModel para interacción con la base de datos MySQL
* **Organización**
	* El Proyecto de código debe estar organizado, es decir, no se debe colocar todo en un solo archivo, sino que se debe dividir la organización del proyecto de acuerdo a las mejores prácticas
* **Nombres, mayúsculas y minúsculas**
	* Usar Lower-case, kebab-case en la URL
	* Usar snake_case or camelCase en el JSON payload
	* Usar nombres en prural para las collecciones/entidades
* **Idempotente y seguridad**
	* GET / HEAD / OPTIONS deben ser seguros (no side-effects)
	* PUT & DELETE debe ser idempotente (same result if replayed)
* **Manejo de errores**
	* Los errores deben ser específicos 
		* **200**  OK – Normal, Exitoso
		* **201**  Created – Retorna el nuevo recurso en el Body y el location header.
		* **204**  No Content – Para DELETE o vacío PUT/PATCH
		* **400**  Bad Request – El payload es incorrecto
		* **401**  Unauthorized – Le hace falta o hay un error en la autenticación
		* **403**  Forbidden – Autenticación correcta pero no está permitido el acceso
		* **404**  Not Found – URL o recurso no encontrado
		* **409**  Conflict – Violación de regla de negocio (Ejemplo; duplicate e-mail, optimistic-lock)
		* **422**  Unprocessable Entity – Error de validación en las entidades
		* **429**  Too Many Requests – Alcanzó la cantidad de peticiones permitidas (rate-limit hit)
		* **500**  Internal Server Error – Error interno del servidor. No se debe exponer información del stack-trace o debug.
		* **502/503/504**– Problemas de ancho de banda
* **Paginación, filtrado y ordenamiento**
	* Siempre paginar
	* Ofrecer el total de conteo mediante la cabecera X-Total-Count 
	* Permitir filtrado en las peticiones Get
	* Permitir ordenamiento en las peticiones GET
	* Permitir busquedas
* **Autenticación y autorización**
	* Usar OAuth 2.1 + Bearer token (JWT or opaque) sin reinventar cabeceras
	* TLS 1.3 cuando sea posble, HSTS, redireccionar peticiones http a https
	* Imprementar Rate-limit por token o IP retornando cabeceras: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
	* Impelemntar CORS creando una lista de acceso permitida de orígenes
* **Observabilidad**
	* Logs estructurados con información detallada del error.
	* Logs de las peticiones: timestamp, method, route, status, duration_ms, user_id, request_id
* **Base de datos**
	* La API tendrá persistencia de datos usando MySQL

## Alcance inicial
* Que permita un CRUD (Create (Post), Read (Get), Update (Put), Delete (Delete)) para las entidades: Usuario y Producto

## Base de datos
### Entidades
#### Usuario
* Id
* Usuario
* Nombre
* Clave
* Perfil
* FechaCreacion
* FechaActualizacion
 
#### Producto
* Id
* Nombre
* Descripcion
* Precio
* FechaCreacion
* FechaActualizacion

## Comandos
* Script para crear base de datos MySQL
	* Para crear la base de datos mysql con persistencia en docker usar la siguiente sentencia:
		```Docker
		docker run -d \
		--name mysql-container \
		-e MYSQL_ROOT_PASSWORD=Root12345 \
		-e MYSQL_DATABASE=Sistema \
		-v mysql_data:/var/lib/mysql \
		-p 3306:3306 \
		mysql:8.0
		```
* Entorno:
	* ``python3 -m venv .venv``
	* ``source .venv/bin/activate``
* Requisitos:
	* ``pip3 install -r requirements.txt``
 * Ejecución:
	* ``source .venv/bin/activate && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload``

# Prueba Técnica — Ingeniero de Datos

Este proyecto implementa una solución completa de **extracción y transformación de datos (ETL)**, una **API REST** para exponer los datos, y un **Agente de IA** que permite realizar consultas en lenguaje natural.  

El repositorio está organizado en cuatro partes:

```graphql
project/
├── etl/ # Parte 1 - ETL (Extracción y carga en SQLite)
├── api/ # Parte 2 - API REST con FastAPI
├── agent/ # Parte 3 - Agente de IA con HuggingFace
├── docs/ # Parte 4 - Analisis de seguridad y proteccion de datos
└── requirements.txt
```

---

## Instalación

1. Clonar el repositorio.  
2. Instalar dependencias:  
   ```bash
   pip install -r requirements.txt
    ```

---

Parte 1 — ETL
Objetivo:

Extraer datos públicos de una API abierta (ejemplo: artículos JSON).

Transformar los registros en un formato normalizado:

```pgsql
id, title, date, author, location, type, summary
```

Guardar los resultados en una base de datos SQLite (etl/db_kitsune.db).

Observacion:

Se usó SQLite por simplicidad (no requiere servidor externo).

Se mantuvo una ruta relativa (db_kitsune.db dentro de etl/) para portabilidad.

Ejecución:

```bash
cd etl
python main.py
```

Esto descarga los registros, los normaliza y los almacena en la base de datos local.

---

**Parte 2 — API REST**

**Objetivo:**

Exponer la base de datos a través de una API construida con FastAPI.

Endpoints principales:

GET /articles → Listar registros (con paginación).

GET /articles/{id} → Consultar registro por ID.

GET /search?q=palabra → Buscar registros por palabra clave.

POST /update → Ejecutar nuevamente el ETL y actualizar la BD.

**Autenticación:**

Soporta tres métodos de autenticación en /update:

Token simple en header (X-Token: mi_token).

Clave en query param (?key=mi_token).

Autenticación básica (user:pass).

**Ejecución (desde carpeta /PruebaKitsune_JEB):**

```bash
uvicorn api.main:app --reload
```
La API estará disponible en: http://127.0.0.1:8000/docs

---

**Parte 3 — Agente de IA**

Objetivo:

Permitir consultas en lenguaje natural que el agente interpreta y transforma en llamadas a la API.

**Características:**

Usa un modelo de HuggingFace (facebook/bart-large-mnli) para zero-shot classification.

Identifica la intención del usuario:

listar → llama a /articles.

buscar → llama a /search?q=palabra.

detalle → llama a /articles/{id}.

Devuelve un resumen claro (máx. 5 resultados para listar, y todos los posibles en buscar).

Si la consulta es ambigua, pide aclaración.

**Observacion:**

Se eligió HuggingFace en lugar de OpenAI para tener una solución open source y gratuita.

Se mantuvo todo con rutas relativas para que el proyecto funcione al descargarlo en cualquier equipo.

Ejecución:

En una terminal, corre la API (desde carpeta /PruebaKitsune_JEB).

```bash
uvicorn api.main:app --reload
```

En otra terminal, corre el agente:

```bash
cd agent
python agent.py
```

Ejemplos de uso:

```shell
> Muéstrame el articulo 33121
> Lista articulos
> Busca articulos sobre NASA
```
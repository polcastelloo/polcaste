# Team Challenge SQL — NovaTech

Práctica del Bootcamp AI Engineering (The Bridge). Dos partes independientes:

- **`Parte_I_SQL_Game.ipynb`** — SQL Murder Mystery: investigación resuelta con queries sobre
  `data/sql-murder-mystery.db`. Caso resuelto: **Miranda Priestly**, que contrató a Jeremy Bowers
  para cometer el asesinato.
- **`parte_2_modelo_bigquery/`** — Diseño e implementación desde cero de una base de datos
  relacional normalizada a 3NF para **NovaTech**, un e-commerce de electrónica, implementada en
  Google BigQuery.

## Estructura del repositorio

```
03_Practica_Obligatoria SQL/
├── Parte_I_SQL_Game.ipynb
├── parte_2_modelo_bigquery/
│   ├── docs/
│   │   ├── er_diagram.png
│   │   └── normalizacion.md
│   └── notebooks/
│       ├── 01_setup_bigquery.ipynb
│       ├── 02_generate_data.ipynb
│       └── 03_queries_verification.ipynb
├── seed.py
├── data/
│   └── sql-murder-mystery.db   (solo usado por la Parte 1)
├── .env.example
├── .gitignore
└── requirements.txt
```

## Setup

```bash
# 1. Entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Dependencias
pip install -r requirements.txt

# 3. Credenciales de BigQuery (solo necesarias para la Parte 2)
cp .env.example .env
# Editar .env con tu GCP_PROJECT_ID y la ruta al JSON del service account
```

Para la Parte 2 hace falta:

1. Un proyecto de Google Cloud con la API de BigQuery activada.
2. Un Service Account con rol `BigQuery Admin` y su clave JSON descargada
   (guardarla en `credentials/`, que ya está en `.gitignore` — nunca subir este fichero).
3. Rellenar `.env` con `GCP_PROJECT_ID`, `BQ_DATASET_ID` (por defecto `novatech`) y
   `GOOGLE_APPLICATION_CREDENTIALS`.

## Cómo ejecutar la Parte 2

En este orden:

1. `parte_2_modelo_bigquery/notebooks/01_setup_bigquery.ipynb` — crea el dataset y las 8 tablas.
2. `parte_2_modelo_bigquery/notebooks/02_generate_data.ipynb` — genera datos sintéticos con
   Faker (500 clientes, 70 productos, 2000 pedidos) y los carga en BigQuery.
3. `parte_2_modelo_bigquery/notebooks/03_queries_verification.ipynb` — queries analíticas
   (ingresos/margen por categoría, segmentación de clientes, satisfacción, incidencias de pago
   y envío) que verifican que el modelo responde a las necesidades de negocio.

Alternativa: ejecutar todo de una vez con el script bonus:

```bash
python seed.py --project mi-proyecto --dataset novatech --customers 500 --products 70 --orders 2000
```

## Modelo de datos

Ver `parte_2_modelo_bigquery/docs/er_diagram.png` para el diagrama entidad-relación completo y
`parte_2_modelo_bigquery/docs/normalizacion.md` para la justificación de 1NF/2NF/3NF.

8 entidades: `categories`, `products`, `customers`, `orders`, `order_items`, `payments`,
`shipments`, `reviews`.

## Coste

Diseñado para no generar ningún coste: los volúmenes usados (~500 clientes, 70 productos,
2000 pedidos) están muy por debajo del Free Tier permanente de BigQuery (10 GB de
almacenamiento y 1 TB de queries procesadas al mes). Ver `guia_tc_sql.html` para el detalle.

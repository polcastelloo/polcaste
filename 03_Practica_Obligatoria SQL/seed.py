#!/usr/bin/env python3
"""
seed.py — Regenera desde cero la base de datos NovaTech en BigQuery.

Crea el dataset y las 8 tablas (si no existen) y las puebla con datos
sinteticos generados con Faker, respetando la integridad referencial.

Uso:
    python seed.py --project mi-proyecto --dataset novatech \
        --customers 500 --products 70 --orders 2000

Requiere las mismas variables que 01_setup_bigquery.ipynb / 02_generate_data.ipynb
si no se pasan por CLI: lee GOOGLE_APPLICATION_CREDENTIALS del .env (o del entorno)
para autenticar contra BigQuery.
"""
import argparse
import os
import random
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from faker import Faker
from google.cloud import bigquery
from google.oauth2 import service_account

COUNTRIES = ["Spain", "France", "Germany", "Italy", "Portugal", "Netherlands"]
COUNTRY_WEIGHTS = [0.40, 0.15, 0.15, 0.12, 0.10, 0.08]
CHANNELS = ["organic", "paid_ads", "social_media", "referral", "email_marketing"]
CHANNEL_WEIGHTS = [0.30, 0.25, 0.20, 0.15, 0.10]
ORDER_STATUSES = ["delivered", "shipped", "processing", "pending", "cancelled"]
ORDER_STATUS_WEIGHTS = [0.65, 0.12, 0.08, 0.08, 0.07]
PAYMENT_METHODS = ["credit_card", "paypal", "bank_transfer"]
CARRIERS = ["SEUR", "Correos Express", "DHL", "GLS", "UPS"]

CATEGORY_DEFS = [
    ("Smartphones", "Telefonos moviles y accesorios de conectividad"),
    ("Laptops", "Portatiles para uso personal, gaming y profesional"),
    ("Audio", "Auriculares, altavoces y equipos de sonido"),
    ("Wearables", "Relojes inteligentes y pulseras de actividad"),
    ("Tablets", "Tablets y accesorios de escritura/dibujo digital"),
    ("Gaming", "Consolas, mandos y perifericos de videojuegos"),
    ("Accesorios", "Cables, fundas, cargadores y complementos"),
    ("Fotografia", "Camaras, drones y accesorios fotograficos"),
]
PRODUCT_WORDS = {
    "Smartphones": ["Phone", "Mobile", "Edge", "Nova", "Pulse"],
    "Laptops": ["Book", "Pro", "Air", "Flex", "Studio"],
    "Audio": ["Buds", "Sound", "Beat", "Wave", "Tone"],
    "Wearables": ["Watch", "Band", "Fit", "Track", "Pulse"],
    "Tablets": ["Tab", "Pad", "Slate", "Canvas", "Note"],
    "Gaming": ["Play", "Pad", "Controller", "Arcade", "Console"],
    "Accesorios": ["Cable", "Case", "Charger", "Mount", "Hub"],
    "Fotografia": ["Cam", "Lens", "Shot", "Drone", "Frame"],
}
BRANDS = ["Zenlo", "Kortex", "Vantix", "Orbeon", "Nyra", "Halion", "Drakon", "Ecliptic"]
RATING_WEIGHTS = [0.04, 0.06, 0.15, 0.35, 0.40]
COMMENTS_POS = [
    "Muy buena calidad, volveria a comprar.",
    "Llego antes de lo esperado, encantado.",
    "Relacion calidad-precio excelente.",
    "Tal cual se describe, sin sorpresas.",
]
COMMENTS_NEG = [
    "No cumplio mis expectativas.",
    "Llego con un golpe en la caja.",
    "El producto tarda en cargar mas de lo anunciado.",
    "Atencion al cliente lenta.",
]

SCHEMAS = {
    "categories": [
        bigquery.SchemaField("category_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
    ],
    "customers": [
        bigquery.SchemaField("customer_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("first_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("last_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("country", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("city", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("acquisition_channel", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("registration_date", "DATE", mode="REQUIRED"),
    ],
    "products": [
        bigquery.SchemaField("product_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("category_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("sku", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("unit_price", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("unit_cost", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("stock_quantity", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("is_active", "BOOL", mode="REQUIRED"),
    ],
    "orders": [
        bigquery.SchemaField("order_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("customer_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("order_date", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
    ],
    "order_items": [
        bigquery.SchemaField("order_item_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("order_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("product_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("quantity", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("unit_price", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("unit_cost", "FLOAT64", mode="REQUIRED"),
    ],
    "payments": [
        bigquery.SchemaField("payment_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("order_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("amount", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("payment_date", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("method", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
    ],
    "shipments": [
        bigquery.SchemaField("shipment_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("order_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("carrier", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("shipped_date", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("delivered_date", "TIMESTAMP", mode="NULLABLE"),
    ],
    "reviews": [
        bigquery.SchemaField("review_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("product_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("customer_id", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("rating", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("comment", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("review_date", "DATE", mode="REQUIRED"),
    ],
}
CREATION_ORDER = [
    "categories", "customers", "products", "orders",
    "order_items", "payments", "shipments", "reviews",
]


def parse_args():
    p = argparse.ArgumentParser(description="Regenera la base de datos NovaTech en BigQuery.")
    p.add_argument("--project", default=os.getenv("GCP_PROJECT_ID"), help="ID del proyecto GCP")
    p.add_argument("--dataset", default=os.getenv("BQ_DATASET_ID", "novatech"), help="ID del dataset")
    p.add_argument("--credentials", default=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
                   help="Ruta al JSON del service account")
    p.add_argument("--customers", type=int, default=500)
    p.add_argument("--products", type=int, default=70)
    p.add_argument("--orders", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def build_dataframes(n_customers, n_products, n_orders, seed):
    random.seed(seed)
    fake = Faker()
    Faker.seed(seed)

    today = datetime(2025, 1, 1)
    one_year_ago = today - timedelta(days=365)

    df_categories = pd.DataFrame([
        {"category_id": i + 1, "name": name, "description": desc}
        for i, (name, desc) in enumerate(CATEGORY_DEFS)
    ])

    products_rows = []
    for pid in range(1, n_products + 1):
        category = df_categories.sample(1, random_state=pid).iloc[0]
        word = random.choice(PRODUCT_WORDS[category["name"]])
        brand = random.choice(BRANDS)
        name = f"{brand} {word} {random.choice(['X', 'Pro', 'Lite', 'Max', '2'])}"
        unit_cost = round(random.uniform(15, 900), 2)
        margin_pct = random.uniform(0.25, 0.70)
        unit_price = round(unit_cost / (1 - margin_pct), 2)
        products_rows.append({
            "product_id": pid, "category_id": int(category["category_id"]),
            "name": name, "sku": f"NVT-{pid:04d}",
            "unit_price": unit_price, "unit_cost": unit_cost,
            "stock_quantity": random.randint(0, 500),
            "is_active": random.random() > 0.05,
        })
    df_products = pd.DataFrame(products_rows)

    customers_rows = []
    for cid in range(1, n_customers + 1):
        country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]
        first, last = fake.first_name(), fake.last_name()
        reg_date = fake.date_between(start_date=one_year_ago - timedelta(days=365), end_date=one_year_ago)
        customers_rows.append({
            "customer_id": cid, "first_name": first, "last_name": last,
            "email": f"{first.lower()}.{last.lower()}{cid}@example.com",
            "country": country, "city": fake.city(),
            "acquisition_channel": random.choices(CHANNELS, weights=CHANNEL_WEIGHTS, k=1)[0],
            "registration_date": reg_date,
        })
    df_customers = pd.DataFrame(customers_rows)

    orders_rows, order_items_rows = [], []
    order_item_id = 1
    active_products = df_products[df_products["is_active"]].reset_index(drop=True)
    for oid in range(1, n_orders + 1):
        customer_id = random.randint(1, n_customers)
        order_date = fake.date_time_between(start_date=one_year_ago, end_date=today)
        status = random.choices(ORDER_STATUSES, weights=ORDER_STATUS_WEIGHTS, k=1)[0]
        orders_rows.append({"order_id": oid, "customer_id": customer_id, "order_date": order_date, "status": status})
        n_items = random.randint(1, 4)
        chosen = active_products.sample(n=min(n_items, len(active_products)), replace=False)
        for _, prod in chosen.iterrows():
            order_items_rows.append({
                "order_item_id": order_item_id, "order_id": oid, "product_id": int(prod["product_id"]),
                "quantity": random.randint(1, 3), "unit_price": prod["unit_price"], "unit_cost": prod["unit_cost"],
            })
            order_item_id += 1
    df_orders = pd.DataFrame(orders_rows)
    df_order_items = pd.DataFrame(order_items_rows)

    order_totals = (
        df_order_items.assign(line_total=lambda d: d["quantity"] * d["unit_price"])
        .groupby("order_id")["line_total"].sum()
    )
    payments_rows, payment_id = [], 1
    for _, order in df_orders.iterrows():
        oid, total, order_date = order["order_id"], round(float(order_totals.get(order["order_id"], 0.0)), 2), order["order_date"]
        if order["status"] == "cancelled":
            payments_rows.append({"payment_id": payment_id, "order_id": oid, "amount": total,
                                   "payment_date": order_date, "method": random.choice(PAYMENT_METHODS), "status": "failed"})
            payment_id += 1
            continue
        r = random.random()
        if r < 0.05:
            payments_rows.append({"payment_id": payment_id, "order_id": oid, "amount": total,
                                   "payment_date": order_date, "method": random.choice(PAYMENT_METHODS), "status": "failed"})
            payment_id += 1
            payments_rows.append({"payment_id": payment_id, "order_id": oid, "amount": total,
                                   "payment_date": order_date + timedelta(minutes=random.randint(5, 120)),
                                   "method": random.choice(PAYMENT_METHODS), "status": "completed"})
            payment_id += 1
        elif r < 0.08 and order["status"] == "delivered":
            payments_rows.append({"payment_id": payment_id, "order_id": oid, "amount": total,
                                   "payment_date": order_date, "method": random.choice(PAYMENT_METHODS), "status": "refunded"})
            payment_id += 1
        else:
            payments_rows.append({"payment_id": payment_id, "order_id": oid, "amount": total,
                                   "payment_date": order_date, "method": random.choice(PAYMENT_METHODS), "status": "completed"})
            payment_id += 1
    df_payments = pd.DataFrame(payments_rows)

    shipments_rows, shipment_id = [], 1
    for _, order in df_orders.iterrows():
        if order["status"] not in ("shipped", "delivered"):
            continue
        shipped_date = order["order_date"] + timedelta(days=random.randint(1, 3))
        delivered_date, ship_status = None, "in_transit"
        if order["status"] == "delivered":
            delivered_date = shipped_date + timedelta(days=random.randint(1, 6))
            ship_status = "delivered"
        shipments_rows.append({"shipment_id": shipment_id, "order_id": order["order_id"], "carrier": random.choice(CARRIERS),
                                "status": ship_status, "shipped_date": shipped_date, "delivered_date": delivered_date})
        shipment_id += 1
    df_shipments = pd.DataFrame(shipments_rows)

    reviews_rows, review_id = [], 1
    delivered_orders = df_orders[df_orders["status"] == "delivered"]
    delivered_items = df_order_items[df_order_items["order_id"].isin(delivered_orders["order_id"])]
    for _, item in delivered_items.iterrows():
        if random.random() > 0.40:
            continue
        order = delivered_orders[delivered_orders["order_id"] == item["order_id"]].iloc[0]
        rating = random.choices([1, 2, 3, 4, 5], weights=RATING_WEIGHTS, k=1)[0]
        comment = random.choice(COMMENTS_POS) if rating >= 4 else random.choice(COMMENTS_NEG)
        review_date = order["order_date"] + timedelta(days=random.randint(7, 30))
        reviews_rows.append({"review_id": review_id, "product_id": int(item["product_id"]),
                              "customer_id": int(order["customer_id"]), "rating": rating, "comment": comment,
                              "review_date": review_date.date()})
        review_id += 1
    df_reviews = pd.DataFrame(reviews_rows)

    return {
        "categories": df_categories, "customers": df_customers, "products": df_products,
        "orders": df_orders, "order_items": df_order_items, "payments": df_payments,
        "shipments": df_shipments, "reviews": df_reviews,
    }


def main():
    load_dotenv()
    args = parse_args()
    if not args.project:
        raise SystemExit("Falta --project (o GCP_PROJECT_ID en el .env)")
    if not args.credentials:
        raise SystemExit("Falta --credentials (o GOOGLE_APPLICATION_CREDENTIALS en el .env)")

    credentials = service_account.Credentials.from_service_account_file(args.credentials)
    client = bigquery.Client(project=args.project, credentials=credentials)

    dataset_ref = bigquery.Dataset(f"{args.project}.{args.dataset}")
    dataset_ref.location = "EU"
    client.create_dataset(dataset_ref, exists_ok=True)
    print(f"Dataset '{args.dataset}' listo")

    for table_name in CREATION_ORDER:
        table_ref = f"{args.project}.{args.dataset}.{table_name}"
        table = bigquery.Table(table_ref, schema=SCHEMAS[table_name])
        client.create_table(table, exists_ok=True)
    print("Tablas creadas")

    dataframes = build_dataframes(args.customers, args.products, args.orders, args.seed)

    for table_name in CREATION_ORDER:
        df = dataframes[table_name]
        table_ref = f"{args.project}.{args.dataset}.{table_name}"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        print(f"{table_name}: {len(df)} filas cargadas")

    print("\nSeed completo.")


if __name__ == "__main__":
    main()

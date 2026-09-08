# Normalización — NovaTech (e-commerce de electrónica)

## Entidades

| Tabla | Descripción |
|---|---|
| `categories` | Categorías de producto (Smartphones, Laptops, Audio, Wearables, ...) |
| `products` | Catálogo, con precio de venta, coste y stock |
| `customers` | Clientes: contacto, país/ciudad, canal de adquisición |
| `orders` | Cabecera de pedido: cliente, fecha, estado |
| `order_items` | Líneas de pedido (relación N:M entre `orders` y `products`) |
| `payments` | Pagos asociados a un pedido (permite reembolsos / reintentos) |
| `shipments` | Envíos asociados a un pedido (permite envíos parciales) |
| `reviews` | Valoraciones de producto hechas por un cliente |

## 1NF — Primera Forma Normal

Todos los campos son atómicos: no hay listas ni valores combinados en una misma columna
(por ejemplo, no existe una columna `productos_comprados = "1001,1002,1003"`).

El caso más claro es el pedido: en lugar de tener columnas repetidas `producto_1, cantidad_1,
producto_2, cantidad_2, ...` en `orders` (un grupo repetido), cada línea de un pedido es una
fila independiente en `order_items`. Esto también resuelve la relación N:M real que existe
entre pedidos y productos (un pedido tiene varios productos, un producto aparece en varios
pedidos).

## 2NF — Segunda Forma Normal

Todas las tablas usan una **clave primaria simple (surrogate key)**: `customer_id`,
`product_id`, `order_id`, `order_item_id`, etc. Al no haber claves primarias compuestas,
no puede darse una dependencia *parcial* de un atributo respecto a solo una parte de la
clave.

El caso a justificar es `order_items`: conceptualmente su clave de negocio es el par
(`order_id`, `product_id`), y tanto `quantity` como `unit_price`/`unit_cost` dependen de
**ese par completo**, no de uno de los dos por separado — es decir, `quantity` no tiene
sentido sin saber tanto el pedido como el producto. Uso `order_item_id` como PK técnica,
pero la dependencia funcional sigue siendo respecto a la clave de negocio completa, por lo
que 2NF se cumple.

## 3NF — Tercera Forma Normal

No debe haber dependencias transitivas (un atributo no-clave que dependa de otro atributo
no-clave, en lugar de depender directamente de la PK).

Decisiones concretas:

- **El nombre/descripción de la categoría no se guarda en `products`**, solo `category_id`.
  Si guardara `category_name` en `products`, ese campo dependería de `category_id`
  (no-clave → no-clave) y no directamente de `product_id`: sería una dependencia transitiva
  y además obligaría a actualizar N filas de `products` si cambia el nombre de una categoría.

- **El país/ciudad del cliente no se repite en `orders`**, solo vive en `customers`. `orders`
  únicamente guarda `customer_id`; para saber el país de un pedido se hace `JOIN` con
  `customers`. Igual con el email o el canal de adquisición.

- **`orders` no almacena un `total_amount`.** El total de un pedido es un valor *derivado*
  (`SUM(quantity * unit_price)` de sus `order_items`), no un hecho atómico del pedido. Si lo
  guardara en `orders`, dependería transitivamente del contenido de `order_items` y
  quedaría desincronizado en cuanto cambiara una línea. Se calcula siempre con una query
  (ver `03_queries_verification.ipynb`).

- **Excepción justificada — `order_items.unit_price` / `unit_cost`:** estos campos
  **sí** duplican, en el momento de la compra, el valor que en ese instante tenía
  `products.unit_price` / `unit_cost`. Esto **no rompe 3NF** porque no es la misma
  información en dos sitios: `products.unit_price` es el precio *actual* (cambia con el
  tiempo), mientras que `order_items.unit_price` es un **hecho histórico** — el precio al
  que se vendió esa unidad en ese pedido concreto. Son dos atributos distintos que
  responden a preguntas distintas ("¿cuánto cuesta hoy?" vs. "¿cuánto pagó el cliente
  entonces?"). Sin este snapshot, cualquier cambio de precio futuro falsearía el histórico
  de ingresos y márgenes.

## Cardinalidades (ver `docs/er_diagram.png`)

- `categories` 1:N `products`
- `customers` 1:N `orders`
- `customers` 1:N `reviews`
- `orders` 1:N `order_items` — `products` 1:N `order_items` (N:M orders↔products)
- `orders` 1:N `payments` (permite pagos fallidos / reembolsos como filas adicionales)
- `orders` 1:N `shipments` (permite envíos parciales)
- `products` 1:N `reviews`

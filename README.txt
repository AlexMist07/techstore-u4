# TechStore U4 - Núcleo de Negocio y API REST

##  Descripción del Proyecto
Implementación del núcleo de lógica de negocio para la empresa **TechStore** en el marco de la Unidad 4. El desarrollo aplica los principios de **Domain-Driven Design (DDD)**, validación de reglas comerciales mediante el **Patrón Specification**, una **Máquina de Estados** robusta con emisión de **Eventos de Dominio (Domain Events)** y una interfaz **API REST** desarrollada con **FastAPI**.

---

##  Estructura del Repositorio
text
techstore-u4/
├── app/
│   ├── init.py          # Inicializador de paquete Python
│   ├── domain.py            # Entidades, Value Objects, Excepciones y Máquina de Estados
│   ├── specifications.py    # Patrón Specification y operadores lógicos (&, |, ~)
│   └── api.py               # API REST construida con FastAPI y mapeo de errores HTTP
├── datos/
│   ├── clientes.csv         # 12 clientes (es_vip, activo)
│   ├── detalle_pedidos.csv  # 21 renglones de detalle de productos por pedido
│   ├── escenarios.csv       # 15 escenarios de prueba E01-E15
│   ├── pedidos.csv          # 16 pedidos iniciales (estado DRAFT)
│   └── productos.csv        # 12 productos del catálogo (precios MXN)
├── tests/
│   ├── test_domain.py       # Pruebas unitarias de reglas de dominio y Specifications
│   └── test_api.py          # Pruebas de integración HTTP (200, 404, 409, 422)
├── cargar_csv.py            # Script cargador de datos desde CSV a memoria
└── README.md                # Documentación técnica y guía de ejecución

---

##  Requisitos e Instalación
1. Tener instalado **Python 3.11 o superior**.
2. Clonar el repositorio y configurar las dependencias necesarias en tu entorno virtual o terminal:

bash
pip install fastapi uvicorn pytest httpx

---

##  Guía de Ejecución

### 1. Carga Inicial de Datos (Prueba CSV)
Para verificar la instanciación correcta de los 16 pedidos iniciales en memoria en estado `DRAFT`:

bash
python cargar_csv.py


### 2. Ejecución de Pruebas Automáticas (Pytest)
Para validar la suite completa de pruebas unitarias e integrales (dominio y API):

bash
python -m pytest -v


### 3. Ejecución del Servidor Local (API REST)
Para levantar el servidor web interactivo con Uvicorn:

bash
python -m uvicorn app.api:app --reload

Una vez iniciado, abre tu navegador y accede a la interfaz de documentación interactiva en Swagger UI:
 **`http://127.0.0.1:8000/docs`**

---

##  Endpoints de la API REST
* **`GET /orders/{order_id}`**: Consulta el estado actual, cliente y detalles de un pedido.
* **`POST /orders/{order_id}/confirm`**: Ejecuta la transición de `DRAFT` a `CONFIRMED` y emite el evento inmutable `OrderConfirmed`.
* **`POST /orders/{order_id}/ship`**: Realiza la transición a `SHIPPED` requiriendo un número de guía válido.
* **`POST /orders/{order_id}/cancel`**: Cancela un pedido con su respectivo motivo registrado.

---

##  Reglas de Negocio Implementadas
* **Precisión Financiera:** Uso estricto del tipo `Decimal` (evitando `float`) para prevenir errores de redondeo en importes y subtotales.
* **Límite de Unidades:** Restricción estricta de un máximo de **20 unidades físicas** acumuladas por pedido.
* **Patrón Specification:** Encapsulamiento dinámico de reglas comerciales para descuentos (10% para clientes VIP con compras mayores a $500 MXN y 4+ unidades; 5% por volumen superior a $5,000 MXN).
* **Gestión de Estados y Excepciones:** Control riguroso de transiciones legales de la máquina de estados y mapeo semántico de errores HTTP (`404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`).
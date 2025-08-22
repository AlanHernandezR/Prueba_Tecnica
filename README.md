# 🚀 API de Gestión de Pedidos

Esta API permite gestionar pedidos y productos, incluyendo:

- 📦 Creación de pedidos
- 🔍 Consulta de pedidos
- 🗑️ Eliminación de pedidos
- 📊 Generación de reportes de ventas

---

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Instalación](#instalación)
3. [Ejecutar el Servidor](#ejecutar-el-servidor)
4. [Endpoints](#endpoints)
   - [Pedidos](#pedidos)
   - [Reportes](#reportes)
5. [Ejemplos de Respuesta](#ejemplos-de-respuesta)

---

## ✅ Requisitos Previos

- **Python** 3.9 o superior  
- **FastAPI**  
- **SQLModel**  
- Una **base de datos** configurada y conectada al proyecto  

---

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/AlanHernandezR/Prueba_Tecnica.git
   ```

2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```

   Activar el entorno:
   - **Linux/Mac**: `source venv/bin/activate`
   - **Windows**: `venv\Scripts\activate`

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Ejecutar el Servidor

Ejecuta el siguiente comando para iniciar el servidor en modo desarrollo:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Documentación interactiva Swagger)

---

## 📡 Endpoints

### 📦 Pedidos

| Acción                     | Método | URL                  | Descripción                               |
|-----------------------------|--------|----------------------|-------------------------------------------|
| Crear un pedido             | POST   | `/orders/`           | Crea un nuevo pedido con al menos un producto |
| Listar todos los pedidos    | GET    | `/orders/`           | Obtiene todos los pedidos registrados      |
| Obtener un pedido por ID    | GET    | `/orders/{order_id}` | Obtiene un pedido específico por su ID     |
| Eliminar un pedido por ID   | DELETE | `/orders/{order_id}` | Elimina un pedido específico por su ID     |

---

### 📊 Reportes

| Acción                  | Método | URL                      | Descripción                              |
|--------------------------|--------|--------------------------|------------------------------------------|
| Total de ventas          | GET    | `/reports/sales`         | Calcula el total de ventas de todos los productos |
| Productos más vendidos   | GET    | `/reports/top-products`  | Obtiene los **3 productos más vendidos** |

---

## 📝 Ejemplos de Respuesta

### Crear un pedido
**Request**
```json
POST /orders/
{
  "customer_name": "Juan Pérez",
  "items": [
    {"name": "Producto 1", "price": 100.0},
    {"name": "Producto 2", "price": 200.0}
  ]
}
```

**Response**
```json
{
  "status": 201,
  "message": "Pedido creado correctamente."
}
```

---

### Listar pedidos
**Request**
```http
GET /orders/
```

**Response**
```json
{
  "status": 200,
  "message": "Pedidos listados correctamente.",
  "data": [/* Lista de pedidos */]
}
```

---

### Reporte: Total de ventas
**Request**
```http
GET /reports/sales
```

**Response**
```json
{
  "status": 200,
  "message": "Total de ventas calculado correctamente.",
  "data": {"total_ventas": 500.0}
}
```

---

### Reporte: Productos más vendidos
**Request**
```http
GET /reports/top-products
```

**Response**
```json
{
  "status": 200,
  "message": "Top 3 productos más vendidos.",
  "data": [
    {"Nombre": "Producto 1", "vendidos": 10},
    {"Nombre": "Producto 2", "vendidos": 8},
    {"Nombre": "Producto 3", "vendidos": 5}
  ]
}
```

---

## 📌 Notas
- Para explorar y probar la API fácilmente, accede a la interfaz **Swagger UI** en `/docs`.
- También está disponible la documentación en formato **Redoc** en `/redoc`.

---

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from models import Order, Item
from schemas import OrderCreate, OrderRead
from database import get_session
from collections import Counter

router = APIRouter()

# Funcion para validar por si hace falta el nombre o el precio de los productos mayor a 0

def validar_items(items):
    for item in items:
        if not item.name or item.name.strip() == "":
            return "Hace falta el nombre del producto."
        # Validar que el precio sea numérico y decimal si es necesario
        try:
            price = float(item.price)
        except (TypeError, ValueError):
            return "El precio de cada producto debe ser numérico."
        if price <= 0:
            return "El precio de cada producto debe ser mayor a 0."
    return

# Esta ruta se encarga de la creación del pedido con validación de al menos un producto
# Y la validacion de que el producto tenga un precio mayor a 0

@router.post("/orders/", response_model=dict)
def create_order(order_in: OrderCreate, session: Session = Depends(get_session)):
    if not order_in.items or len(order_in.items) == 0:
        return JSONResponse(
            content={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "El pedido debe tener al menos un producto."
            }
        )
    error = validar_items(order_in.items)
    if error:
        return JSONResponse(
            content={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error
            }
        )
    order = Order(customer_name=order_in.customer_name)
    session.add(order)
    session.commit()
    session.refresh(order)
    items = []
    for item_in in order_in.items:
        item = Item(name=item_in.name, price=item_in.price, order_id=order.id)
        session.add(item)
        items.append(item)
    session.commit()
    session.refresh(order)
    order.items = items
    return JSONResponse(
        content={
            "status": status.HTTP_201_CREATED,
            "message": "Pedido creado correctamente."
        }
    )


# Regresa todo el listado de pedidos y sus items
@router.get("/orders/", response_model=dict)
def list_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(Order)).all()
    if not orders:
        return JSONResponse(
            content={
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No se han registrado pedidos."
            }
        )
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK,
            "message": "Pedidos listados correctamente.",
            "data": [OrderRead.model_validate(order).model_dump(mode="json") for order in orders]
        }
    )


# Esta ruta se encarga de obtener un pedido por su ID
@router.get("/orders/{order_id}", response_model=dict)
def get_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        return JSONResponse(
            content={"status": status.HTTP_404_NOT_FOUND, "message": "Pedido no encontrado"}
        )
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK,
            "message": "Pedido encontrado.",
            "data": OrderRead.model_validate(order).model_dump(mode="json")
        }
    )

# Esta ruta se encarga de eliminar un pedido por su ID
@router.delete("/orders/{order_id}", response_model=dict)
def delete_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        return JSONResponse(
            content={"status": status.HTTP_404_NOT_FOUND, "message": "Pedido no encontrado"}
        )
    session.delete(order)
    session.commit()
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK,
            "message": f"Order {order_id} eliminado correctamente."
        }
    )


# Esta ruta se encarga de obtener el total de ventas
@router.get("/reports/sales", response_model=dict)
def get_total_sales(session: Session = Depends(get_session)):
    total = session.exec(select(Item.price)).all()
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK,
            "message": "Total de ventas calculado correctamente.",
            "data": {"total_ventas": sum(total)}
        }
    )


# Esta ruta se encarga de obtener los productos más vendidos
@router.get("/reports/top-products", response_model=dict)
def get_top_products(session: Session = Depends(get_session)):
    
    items = session.exec(select(Item.name)).all()
    if not items:
        return JSONResponse(
            content={
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No se han registrado productos.",
                "data": []
            }
        )
    counter = Counter(items)
    top = counter.most_common(3)
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK,
            "message": "Top 3 productos más vendidos.",
            "data": [{"Nombre": name, "vendidos": count} for name, count in top]
        }
    )

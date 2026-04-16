from django.shortcuts import get_object_or_404

from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro

class CompraService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = get_object_or_404(Inventario, libro=libro)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        return {
            "libro": libro,
            "total": total,
            "stock_actual": inventario.cantidad,
        }

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="", usuario=None):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        if inv.cantidad < cantidad:
            raise ValueError("No hay existencias.")

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_libro(libro)
            .con_cantidad(cantidad)
            .para_envio(direccion)
            .build()
        )

        total = orden.total

        if not self.procesador_pago.pagar(total):
            orden.delete()
            raise ValueError("Error en el pago.")

        inv.cantidad -= cantidad
        inv.save()

        return total

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        if not lista_productos:
            raise ValueError("Debes enviar al menos un producto.")
        primer_producto = lista_productos[0]
        return self.ejecutar_compra(
            libro_id=primer_producto.id,
            cantidad=1,
            direccion=direccion,
            usuario=usuario,
        )
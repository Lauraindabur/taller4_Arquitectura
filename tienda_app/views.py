from django.shortcuts import render
from django.views import View
from .infra.factories import PaymentFactory
from .services import CompraService

class CompraView(View):
    template_name = "tienda_app/compra.html"

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    @property
    def service(self):
        return self.setup_service()

    def get(self, request, libro_id):
        return render(request, self.template_name, self.service.obtener_detalle_producto(libro_id))

    def post(self, request, libro_id):
        try:
            total = self.service.ejecutar_compra(libro_id)
            detalle = self.service.obtener_detalle_producto(libro_id)
            ctx = {
                **detalle,
                "mensaje_exito": f"Compra exitosa. Total: {total}",
                "stock_antes": detalle["stock_actual"] + 1,
                "stock_despues": detalle["stock_actual"],
            }
        except Exception as e:
            detalle = self.service.obtener_detalle_producto(libro_id)
            ctx = {**detalle, "error": str(e)}
        return render(request, self.template_name, ctx)
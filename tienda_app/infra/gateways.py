import datetime
from ..domain.interfaces import ProcesadorPago
import datetime
from ..domain.interfaces import ProcesadorPago


class BancoNacionalProcesador(ProcesadorPago):

    def pagar(self, monto: float) -> bool:
        archivo_log = "pagos_locales_LAURA_INDABUR_GARCIA.log"

        with open(archivo_log, "a") as f:
            f.write(
                f"[{datetime.datetime.now()}] "
                f"Transacción exitosa por: ${monto}\n"
            )

        return True
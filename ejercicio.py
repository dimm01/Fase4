# ============================================================
# MÓDULO 1 - Jose Gregorio Daza Granadillo
# Clases base abstractas, excepciones personalizadas y logs
# ============================================================

from abc import ABC, abstractmethod
import datetime
import os

# ─────────────────────────────────────────────
# SISTEMA DE LOGS (escribe errores en un archivo)
# ─────────────────────────────────────────────

ARCHIVO_LOG = "eventos.log"

def registrar_log(nivel: str, mensaje: str):
    """Escribe un evento en el archivo de logs con fecha y hora."""
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ahora}] [{nivel.upper()}] {mensaje}\n"
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linea)
    print(f"  LOG [{nivel.upper()}]: {mensaje}")


# ─────────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS
# ─────────────────────────────────────────────

class ErrorSistema(Exception):
    """Excepción base del sistema Software FJ."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje
        registrar_log("ERROR", mensaje)

class ErrorDatoInvalido(ErrorSistema):
    """Se lanza cuando un dato no cumple las validaciones."""
    pass

class ErrorClienteNoEncontrado(ErrorSistema):
    """Se lanza cuando no se encuentra un cliente."""
    pass

class ErrorServicioNoDisponible(ErrorSistema):
    """Se lanza cuando el servicio no está disponible."""
    pass

class ErrorReservaInvalida(ErrorSistema):
    """Se lanza cuando una reserva no puede procesarse."""
    pass

class ErrorOperacionNoPermitida(ErrorSistema):
    """Se lanza al intentar una operación no permitida."""
    pass


# ─────────────────────────────────────────────
# CLASE ABSTRACTA BASE
# ─────────────────────────────────────────────
#Como Regla General pueden modificar el codigo sin romper lo que han hecho los demas
# compañeros siempre que se respete los nombres de clase y metodos
class Entidad(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    
    """
    def __init__(self, id_entidad: int):
        self._id = id_entidad
        self._activo = True

    @property
    def id(self):
        return self._id

    @property
    def activo(self):
        return self._activo

    def desactivar(self):
        self._activo = False

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción textual de la entidad."""
        pass

    @abstractmethod
    def validar(self) -> bool:
        """Valida que la entidad tenga datos correctos."""
        pass

    def __str__(self):
        return self.describir()

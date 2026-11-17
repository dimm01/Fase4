print("Bienvenidos al curso de Programación")
print("Universidad Nacional Abierta y a Distancia")
print("Profesor: Yahith Yamid Gutierrez Gomez ")

# ============================================================
# MÓDULO 1 - Jose Gregorio Daza Granadillo
# Clases base abstractas, excepciones personalizadas y logs
# ============================================================

from abc import ABC, abstractmethod
import datetime
import os
import logging
import re
import unicodedata
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


"""
Modulo 2 - Clase Cliente
Proyecto: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa simulada: Software FJ

Responsabilidad:
- Proteger los datos personales mediante encapsulacion.
- Validar la informacion antes de almacenarla en el objeto.
- Permitir consultar y actualizar los datos de forma controlada.

Este modulo no utiliza bases de datos. Los clientes se representan como
objetos en memoria, de acuerdo con los requisitos del proyecto.
"""


# Se utiliza el logger general del proyecto. El modulo de logs del equipo
# puede configurar sus manejadores y el archivo de destino.
logger = logging.getLogger(__name__)


class Cliente:
    """Representa un cliente registrado en el sistema Software FJ."""

    def __init__(self, documento: str, nombre: str, correo: str, telefono: str):
        # Los atributos privados evitan la modificacion directa desde fuera.
        self.__documento = self._validar_documento(documento)
        self.__nombre = self._validar_nombre(nombre)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

        logger.info("Cliente creado correctamente. Documento: %s", self.__documento)

    @staticmethod
    def _validar_documento(documento: str) -> str:
        """Comprueba que el documento contenga entre 5 y 15 digitos."""
        if not isinstance(documento, str):
            raise TypeError("El documento debe recibirse como texto.")

        documento = documento.strip()
        if not documento.isdigit() or not 5 <= len(documento) <= 15:
            raise ValueError(
                "Documento invalido: debe contener entre 5 y 15 digitos, sin puntos ni espacios."
            )
        return documento

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        """Acepta nombres con letras, espacios, tildes, guiones y apostrofes."""
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe recibirse como texto.")

        nombre = " ".join(nombre.split())
        if not nombre or len(nombre) < 2 or len(nombre) > 80:
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres.")

        # Se admiten letras Unicode y separadores habituales en nombres.
        for caracter in nombre:
            if not (caracter.isalpha() or caracter in " -'’"):
                raise ValueError("El nombre solo puede contener letras, espacios, guiones o apostrofes.")
        return nombre.title()

    @staticmethod
    def _validar_correo(correo: str) -> str:
        """Valida una estructura basica de correo electronico."""
        if not isinstance(correo, str):
            raise TypeError("El correo electronico debe recibirse como texto.")

        correo = correo.strip().lower()
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.fullmatch(patron, correo):
            raise ValueError("Correo electronico invalido. Ejemplo: usuario@dominio.com.")
        return correo

    @staticmethod
    def _validar_telefono(telefono: str) -> str:
        """Acepta de 7 a 15 digitos; permite espacios y el signo + al inicio."""
        if not isinstance(telefono, str):
            raise TypeError("El telefono debe recibirse como texto.")

        telefono = telefono.strip()
        normalizado = telefono.replace(" ", "").replace("-", "")
        if normalizado.startswith("+"):
            digitos = normalizado[1:]
        else:
            digitos = normalizado

        if not digitos.isdigit() or not 7 <= len(digitos) <= 15:
            raise ValueError("Telefono invalido: debe contener entre 7 y 15 digitos.")
        return telefono

    @property
    def documento(self) -> str:
        """Devuelve el documento sin permitir modificarlo directamente."""
        return self.__documento

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        self.__nombre = self._validar_nombre(nuevo_nombre)
        logger.info("Nombre del cliente actualizado. Documento: %s", self.__documento)

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo: str) -> None:
        self.__correo = self._validar_correo(nuevo_correo)
        logger.info("Correo del cliente actualizado. Documento: %s", self.__documento)

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono: str) -> None:
        self.__telefono = self._validar_telefono(nuevo_telefono)
        logger.info("Telefono del cliente actualizado. Documento: %s", self.__documento)

    def actualizar_datos(
        self,
        nombre: str = None,
        correo: str = None,
        telefono: str = None
    ) -> None:
        """
        Actualiza uno o varios datos.
        Primero valida todos los valores recibidos y despues aplica los cambios,
        evitando actualizaciones parciales si alguno de ellos es invalido.
        """
        nuevo_nombre = self.__nombre if nombre is None else self._validar_nombre(nombre)
        nuevo_correo = self.__correo if correo is None else self._validar_correo(correo)
        nuevo_telefono = self.__telefono if telefono is None else self._validar_telefono(telefono)

        self.__nombre = nuevo_nombre
        self.__correo = nuevo_correo
        self.__telefono = nuevo_telefono
        logger.info("Datos del cliente actualizados. Documento: %s", self.__documento)

    def obtener_informacion(self) -> dict:
        """Retorna una copia de los datos para consultas del sistema."""
        return {
            "documento": self.__documento,
            "nombre": self.__nombre,
            "correo": self.__correo,
            "telefono": self.__telefono
        }

    def __str__(self) -> str:
        return (
            f"Cliente: {self.__nombre} | Documento: {self.__documento} | "
            f"Correo: {self.__correo} | Telefono: {self.__telefono}"
        )

#Seccion Pruebas Modulo 2
'''def ejecutar_pruebas_cliente() -> None:
    """Pruebas sencillas de registros validos, invalidos y actualizaciones."""
    print("\n--- PRUEBAS DEL MODULO CLIENTE ---")

    try:
        cliente = Cliente(
            documento="1098765432",
            nombre="Maria Fernanda Rodriguez",
            correo="maria.rodriguez@ejemplo.com",
            telefono="+573001234567"
        )
        print("Registro exitoso:")
        print(cliente)

        cliente.correo = "maria.f.rodriguez@ejemplo.com"
        print("\nCorreo actualizado:")
        print(cliente.obtener_informacion())

    except (TypeError, ValueError) as error:
        logger.exception("No fue posible registrar o actualizar el cliente.")
        print(f"Error controlado: {error}")

    # Se intenta crear un cliente con correo invalido para comprobar
    # que el sistema detecta el dato y continua con las siguientes pruebas.
    try:
        Cliente(
            documento="12345678",
            nombre="Carlos Perez",
            correo="correo-no-valido",
            telefono="3101234567"
        )
    except (TypeError, ValueError) as error:
        print(f"\nPrueba de validacion superada: {error}")

    print("\n--- FIN DE LAS PRUEBAS ---")'''

# ============================================================
# MÓDULO 3 - Nairobys Rocha Mora
# Clase abstracta Servicio y tres servicios especializados
# ============================================================

class ErrorCalculoInconsistente(ErrorSistema):
    """Se lanza cuando el cálculo de un costo da un resultado inconsistente."""
    pass


def es_numero_positivo(valor) -> bool:
    """Devuelve True si el valor es un número (no booleano) mayor que cero."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool) and valor > 0


class Servicio(Entidad):
    """Clase abstracta: plantilla de todos los servicios de Software FJ."""

    def __init__(self, id_servicio: int, nombre: str, disponible: bool = True):
        super().__init__(id_servicio)  # guarda el id en la clase base Entidad
        self._nombre = nombre          # atributo protegido (encapsulación)
        self._disponible = disponible  # indica si se puede reservar

    @property
    def nombre(self):
        """Nombre del servicio (solo lectura)."""
        return self._nombre

    @property
    def disponible(self):
        """Indica si el servicio está disponible."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        """Cambia la disponibilidad, validando que sea True o False."""
        if not isinstance(valor, bool):
            raise ErrorDatoInvalido("La disponibilidad debe ser True o False")
        self._disponible = valor
        registrar_log("INFO", f"Servicio '{self._nombre}' disponible = {valor}")

    # --- Métodos que cada servicio DEBE implementar (polimorfismo) ---

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        """Calcula el costo. Sobrecarga: impuesto y descuento son opcionales."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Devuelve la descripción del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self):
        """Valida los datos del servicio; lanza una excepción si son incorrectos."""
        pass

    def validar(self) -> bool:
        """Método exigido por Entidad: valida y devuelve True si todo está bien."""
        self.validar_parametros()
        return True

    # --- Métodos de apoyo compartidos por las clases hijas ---

    def _validar_nombre(self):
        """Valida que el servicio tenga un nombre no vacío."""
        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ErrorDatoInvalido("El servicio necesita un nombre")

    def _verificar_disponible(self):
        """Lanza una excepción si el servicio no se puede usar."""
        if not self._disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{self._nombre}' no está disponible"
            )

    def _validar_duracion(self, duracion):
        """Valida que la duración exista y sea un número mayor que cero."""
        if duracion is None:
            raise ErrorDatoInvalido("Falta la duración del servicio")
        if not es_numero_positivo(duracion):
            raise ErrorCalculoInconsistente("La duración debe ser un número mayor que 0")

    def _aplicar_ajustes(self, subtotal, impuesto, descuento) -> float:
        """Aplica descuento e impuesto al subtotal (try/except/else/finally)."""
        try:
            # El descuento es un porcentaje entre 0 y 1 (0.10 = 10 %)
            if not 0 <= descuento <= 1:
                raise ValueError("El descuento debe estar entre 0 y 1")
            if impuesto < 0:
                raise ValueError("El impuesto no puede ser negativo")
            total = subtotal * (1 - descuento) * (1 + impuesto)
        except (TypeError, ValueError) as error:
            # Encadenamiento de excepciones: se conserva la causa original
            raise ErrorCalculoInconsistente(
                f"No se pudo calcular el costo de '{self._nombre}': {error}"
            ) from error
        else:
            return round(total, 2)  # solo se ejecuta si no hubo error
        finally:
            # Siempre se ejecuta, haya o no error
            registrar_log("INFO", f"Cálculo de costo finalizado para '{self._nombre}'")


class ReservaSala(Servicio):
    """Servicio: reserva de salas. Se cobra por hora."""

    def __init__(self, id_servicio: int, nombre: str, tarifa_hora, capacidad, disponible: bool = True):
        super().__init__(id_servicio, nombre, disponible)
        self._tarifa_hora = tarifa_hora
        self._capacidad = capacidad
        self.validar_parametros()  # no se puede crear una sala inválida
        registrar_log("INFO", f"Servicio creado: {self.describir()}")

    def validar_parametros(self):
        """Valida nombre, tarifa y capacidad de la sala."""
        self._validar_nombre()
        if not es_numero_positivo(self._tarifa_hora):
            raise ErrorDatoInvalido("La tarifa por hora debe ser mayor que 0")
        if not isinstance(self._capacidad, int) or self._capacidad <= 0:
            raise ErrorDatoInvalido("La capacidad debe ser un entero mayor que 0")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        """Costo = tarifa por hora x horas (duración en horas)."""
        self._verificar_disponible()
        self._validar_duracion(duracion)
        subtotal = self._tarifa_hora * duracion
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        return (f"Sala '{self._nombre}' para {self._capacidad} personas, "
                f"tarifa ${self._tarifa_hora:,.0f} por hora")


class AlquilerEquipo(Servicio):
    """Servicio: alquiler de equipos. Se cobra por día más un depósito."""

    def __init__(self, id_servicio: int, nombre: str, tarifa_dia, deposito=0.0, disponible: bool = True):
        super().__init__(id_servicio, nombre, disponible)
        self._tarifa_dia = tarifa_dia
        self._deposito = deposito
        self.validar_parametros()
        registrar_log("INFO", f"Servicio creado: {self.describir()}")

    def validar_parametros(self):
        """Valida nombre, tarifa por día y depósito del equipo."""
        self._validar_nombre()
        if not es_numero_positivo(self._tarifa_dia):
            raise ErrorDatoInvalido("La tarifa por día debe ser mayor que 0")
        if not isinstance(self._deposito, (int, float)) or self._deposito < 0:
            raise ErrorDatoInvalido("El depósito no puede ser negativo")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        """Costo = tarifa por día x días + depósito (duración en días)."""
        self._verificar_disponible()
        self._validar_duracion(duracion)
        subtotal = self._tarifa_dia * duracion + self._deposito
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        return (f"Equipo '{self._nombre}', tarifa ${self._tarifa_dia:,.0f} por día "
                f"con depósito de ${self._deposito:,.0f}")


class AsesoriaEspecializada(Servicio):
    """Servicio: asesoría especializada. El precio depende del nivel del asesor."""

    # Factor que multiplica la tarifa según el nivel del asesor
    FACTORES_NIVEL = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, id_servicio: int, nombre: str, tarifa_hora, nivel: str = "junior", disponible: bool = True):
        super().__init__(id_servicio, nombre, disponible)
        self._tarifa_hora = tarifa_hora
        self._nivel = nivel
        self.validar_parametros()
        registrar_log("INFO", f"Servicio creado: {self.describir()}")

    def validar_parametros(self):
        """Valida nombre, tarifa y nivel del asesor."""
        self._validar_nombre()
        if not es_numero_positivo(self._tarifa_hora):
            raise ErrorDatoInvalido("La tarifa por hora debe ser mayor que 0")
        if self._nivel not in self.FACTORES_NIVEL:
            raise ErrorDatoInvalido(
                f"Nivel inválido '{self._nivel}'. Use: {', '.join(self.FACTORES_NIVEL)}"
            )

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        """Costo = tarifa por hora x factor del nivel x horas."""
        self._verificar_disponible()
        self._validar_duracion(duracion)
        subtotal = self._tarifa_hora * self.FACTORES_NIVEL[self._nivel] * duracion
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        return (f"Asesoría '{self._nombre}' nivel {self._nivel}, "
                f"tarifa base ${self._tarifa_hora:,.0f} por hora")


# ------------------------------------------------------------
# Prueba del módulo 3 (el módulo 5 puede reemplazarla)
# ------------------------------------------------------------
'''def probar_modulo3():
    """Crea los 3 servicios, calcula costos y provoca errores controlados."""
    print("\n--- MÓDULO 3: prueba de servicios ---")
    servicios = [
        ReservaSala(1, "Sala Norte", 50000, 10),
        AlquilerEquipo(2, "Proyector", 30000, deposito=20000),
        AsesoriaEspecializada(3, "Asesoría en Python", 80000, nivel="senior"),
    ]

    # Polimorfismo: la misma llamada funciona distinto en cada servicio
    for servicio in servicios:
        print(servicio.describir())
        print("  Costo de 2 unidades:", servicio.calcular_costo(2))
        print("  Con IVA 19% y 10% de descuento:",
              servicio.calcular_costo(2, impuesto=0.19, descuento=0.10))

    print("\n--- Casos inválidos (el programa NO se detiene) ---")
    try:
        AlquilerEquipo(4, "Portátil", -5000)  # tarifa negativa
    except ErrorDatoInvalido:
        print("Capturado: servicio inválido")

    try:
        servicios[0].calcular_costo(0)  # duración cero
    except ErrorCalculoInconsistente:
        print("Capturado: duración inválida")

    try:
        servicios[2].calcular_costo(2, descuento=1.5)  # descuento imposible
    except ErrorCalculoInconsistente:
        print("Capturado: descuento inconsistente")

    try:
        servicios[1].disponible = False  # se marca como no disponible
        servicios[1].calcular_costo(1)
    except ErrorServicioNoDisponible:
        print("Capturado: servicio no disponible")
        print("--- FIN PRUEBA MÓDULO 3 ---")'''



# ============================================================
# MÓDULO 4 - Belsi Mejia Caro
# Clase Reserva con estados, confirmación y cancelación
# ============================================================

class Reserva(Entidad):
    """Integra Cliente + Servicio. Estados: PENDIENTE -> CONFIRMADA -> PROCESADA / CANCELADA"""

    _contador_reservas = 0

    def __init__(self, id_reserva: int, cliente, servicio, duracion_horas):
        try:
            if cliente is None:
                raise ErrorReservaInvalida("La reserva requiere un cliente válido.")
            if servicio is None:
                raise ErrorReservaInvalida("La reserva requiere un servicio válido.")
            # Usamos la misma función que usa el Módulo 3: es_numero_positivo()
            if not es_numero_positivo(duracion_horas):
                raise ErrorReservaInvalida(f"Duración inválida: {duracion_horas}. Debe ser mayor a 0.")

            super().__init__(id_reserva)
            Reserva._contador_reservas += 1
            self._cliente = cliente
            self._servicio = servicio
            self._duracion = duracion_horas
            self._estado = "PENDIENTE"
            self._costo_total = 0.0

        except (ErrorReservaInvalida, ErrorDatoInvalido) as e:
            registrar_log("ERROR", f"Error al crear Reserva: {e}")
            raise ErrorReservaInvalida(f"No se pudo crear la reserva: {e}") from e
        else:
            registrar_log("INFO", f"Reserva {self.id} creada en estado PENDIENTE")
        finally:
            print(f"--> Intento de creación de reserva finalizado.")

    @property
    def cliente(self): return self._cliente
    @property
    def servicio(self): return self._servicio
    @property
    def duracion(self): return self._duracion
    @property
    def estado(self): return self._estado
    @property
    def costo_total(self): return self._costo_total

    # --- Obligatorios de Entidad ---
    def describir(self) -> str:
        nombre_cliente = getattr(self._cliente, "nombre", str(self._cliente))
        nombre_servicio = getattr(self._servicio, "nombre", str(self._servicio))
        return f"Reserva #{self.id} | Cliente: {nombre_cliente} | Servicio: {nombre_servicio} | Dur: {self._duracion} | Estado: {self._estado} | Costo: ${self._costo_total:,.0f}"

    def validar_parametros(self):
        """Igual que hace el Módulo 3: valida y lanza excepción si algo está mal."""
        if self._cliente is None or self._servicio is None:
            raise ErrorReservaInvalida("Cliente o servicio no puede ser None.")
        if not es_numero_positivo(self._duracion):
            raise ErrorReservaInvalida("Duración inválida.")
        if self._estado not in ["PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"]:
            raise ErrorReservaInvalida(f"Estado inválido: {self._estado}")

    def validar(self) -> bool:
        try:
            self.validar_parametros()
            return True
        except Exception as e:
            registrar_log("ERROR", f"Error en validar() Reserva {self.id}: {e}")
            return False

    # --- Sobrecarga: mismo nombre que Módulo 3, con impuesto y descuento ---
    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """
        Delega el cálculo al Servicio real.
        Ejemplo: Reserva de Sala 50000 x 2h = 100000
        Con impuesto 0.19 y descuento 0.10 = 100000 * 0.90 * 1.19 = 107100
        """
        try:
            total = self._servicio.calcular_costo(self._duracion, impuesto=impuesto, descuento=descuento)
            self._costo_total = round(total, 2)
            return self._costo_total
        except (ErrorServicioNoDisponible, ErrorCalculoInconsistente, ErrorDatoInvalido) as e:
            registrar_log("ERROR", f"Error calculando costo Reserva {self.id}: {e}")
            raise ErrorReservaInvalida(f"Error en cálculo de costo: {e}") from e

    def confirmar(self, impuesto=0.0, descuento=0.0):
        """PENDIENTE -> CONFIRMADA. Solo si el servicio está disponible."""
        try:
            if self._estado != "PENDIENTE":
                raise ErrorOperacionNoPermitida(f"No se puede confirmar. Estado actual: {self._estado}. Debe estar PENDIENTE.")
            # Propiedad real del Módulo 3: .disponible
            if not self._servicio.disponible:
                raise ErrorServicioNoDisponible(f"Servicio {self._servicio.nombre} no disponible.")
            self._estado = "CONFIRMADA"
            self.calcular_costo(impuesto=impuesto, descuento=descuento)
        except (ErrorOperacionNoPermitida, ErrorServicioNoDisponible, ErrorReservaInvalida) as e:
            registrar_log("ERROR", f"Error al confirmar Reserva {self.id}: {e}")
            print(f"❌ No se pudo confirmar: {e}")
            return False
        else:
            registrar_log("INFO", f"Reserva {self.id} CONFIRMADA. Costo: ${self._costo_total:,.0f}")
            print(f"✅ Reserva {self.id} CONFIRMADA - ${self._costo_total:,.0f}")
            return True
        finally:
            print(f"--> Proceso de confirmación finalizado para Reserva {self.id}")

    def cancelar(self, motivo="Sin motivo"):
        """PENDIENTE o CONFIRMADA -> CANCELADA"""
        try:
            if self._estado == "CANCELADA":
                raise ErrorOperacionNoPermitida("La reserva ya está cancelada.")
            if self._estado == "PROCESADA":
                raise ErrorOperacionNoPermitida("No se puede cancelar una reserva ya procesada.")
            self._estado = "CANCELADA"
        except ErrorOperacionNoPermitida as e:
            registrar_log("ERROR", f"Error al cancelar Reserva {self.id}: {e}")
            print(f"❌ No se pudo cancelar: {e}")
            return False
        else:
            registrar_log("INFO", f"Reserva {self.id} CANCELADA. Motivo: {motivo}")
            print(f"✅ Reserva {self.id} CANCELADA. Motivo: {motivo}")
            return True

    def procesar(self):
        """CONFIRMADA -> PROCESADA"""
        try:
            if self._estado != "CONFIRMADA":
                raise ErrorOperacionNoPermitida(f"Solo se puede procesar una reserva CONFIRMADA. Estado actual: {self._estado}")
            self._estado = "PROCESADA"
        except ErrorOperacionNoPermitida as e:
            registrar_log("ERROR", f"Error al procesar Reserva {self.id}: {e}")
            print(f"❌ No se pudo procesar: {e}")
            return False
        else:
            registrar_log("INFO", f"Reserva {self.id} PROCESADA con éxito.")
            print(f"✅ Reserva {self.id} PROCESADA con éxito.")
            return True
        finally:
            print(f"--> Proceso de reserva {self.id} terminado.")

# -------------------------------
# Prueba del módulo 4
# -------------------------------
'''def probar_modulo4():
    """Prueba Módulo 4 con los 3 servicios REALES del Módulo 3."""
    print("\n--- MÓDULO 4: prueba de reservas ---")

    # Cliente simple para probar, hasta que el Módulo 2 se una a main.py
    class ClientePrueba:
        def __init__(self, nombre): self.nombre = nombre

    c1 = ClientePrueba("Cliente de Prueba")

    # Usamos los mismos servicios que creó Nairobys en probar_modulo3()
    s_sala = ReservaSala(1, "Sala Norte", 50000, 10)
    s_equipo = AlquilerEquipo(2, "Proyector", 30000, deposito=20000)
    s_asesoria = AsesoriaEspecializada(3, "Asesoría en Python", 80000, nivel="senior")

    # 1. Sala: 50000 x 2 = 100000
    r1 = Reserva(1, c1, s_sala, 2)
    print(r1)
    r1.confirmar()
    r1.procesar()
    print(r1)

    # 2. Equipo con impuesto 19% y descuento 10%: (30000*2+20000)=80000 -> 80000*0.90*1.19=85680
    r2 = Reserva(2, c1, s_equipo, 2)
    r2.confirmar(impuesto=0.19, descuento=0.10)
    print(r2)
    r2.cancelar("Cliente se arrepintió")
    r2.confirmar()  # Debe fallar: ya está CANCELADA

    # 3. Asesoría senior: 80000*1.5*2 = 240000
    r3 = Reserva(3, c1, s_asesoria, 2)
    r3.confirmar()
    print(r3)

    # 4. Errores controlados, el programa NO se detiene
    print("\n--- Casos inválidos (el programa NO se detiene) ---")
    try:
        r4 = Reserva(4, c1, s_sala, -2)  # duración negativa
    except ErrorReservaInvalida:
        print("Capturado: reserva con duración inválida")

    try:
        r5 = Reserva(5, c1, s_sala, 0)  # duración cero
    except ErrorReservaInvalida:
        print("Capturado: reserva con duración cero")

    # Servicio no disponible
    s_equipo.disponible = False
    r6 = Reserva(6, c1, s_equipo, 1)
    r6.confirmar()  # Debe fallar controlado

    print("--- FIN PRUEBA MÓDULO 4 ---")'''

if __name__ == "__main__":
    # Configuracion basica solo para ejecutar este archivo individualmente.
    # Al integrarlo, el proyecto grupal puede centralizar la configuracion.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    #probar_modulo3()
    #probar_modulo4()
    #ejecutar_pruebas_cliente()



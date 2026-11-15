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

import logging
import re
import unicodedata

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


def ejecutar_pruebas_cliente() -> None:
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

    print("\n--- FIN DE LAS PRUEBAS ---")


if __name__ == "__main__":
    # Configuracion basica solo para ejecutar este archivo individualmente.
    # Al integrarlo, el proyecto grupal puede centralizar la configuracion.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    ejecutar_pruebas_cliente()


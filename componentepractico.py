import abc
import datetime


# ==============================
# LOGS
# ==============================

def registrar_log(mensaje):

    with open("logs_sistema.txt", "a", encoding="utf-8") as archivo:

        tiempo = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        archivo.write(f"[{tiempo}] {mensaje}\n")


# ==============================
# EXCEPCIONES
# ==============================

class SistemaError(Exception):
    pass


class DatosInvalidosError(SistemaError):
    pass


class ServicioNoDisponibleError(SistemaError):
    pass


# ==============================
# CLASES ABSTRACTAS
# ==============================

class EntidadSistema(abc.ABC):

    @abc.abstractmethod
    def obtener_descripcion(self):
        pass


class Servicio(abc.ABC):

    def __init__(self, nombre_servicio, precio_base):

        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base

    @abc.abstractmethod
    def calcular_costo(self, duracion):
        pass


# ==============================
# CLIENTE
# ==============================

class Cliente(EntidadSistema):

    def __init__(self, id_cliente, nombre, email):

        self.__id = id_cliente
        self.__nombre = nombre
        self.email = email

        registrar_log(
            f"Cliente creado: {nombre}"
        )

    @property
    def nombre(self):
        return self.__nombre

    def obtener_descripcion(self):

        return (
            f"{self.__nombre} - ID {self.__id}"
        )


# ==============================
# SERVICIOS
# ==============================

class ReservaSala(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:

            raise DatosInvalidosError(
                "La duración debe ser positiva"
            )

        return (
            self.precio_base * duracion
        ) * 1.19


class AlquilerEquipo(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:

            raise DatosInvalidosError(
                "La duración debe ser positiva"
            )

        return (
            self.precio_base * duracion
        )


class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:

            raise DatosInvalidosError(
                "La duración debe ser positiva"
            )

        return (
            self.precio_base * duracion
        )


# ==============================
# RESERVA
# ==============================

class Reserva:

    def __init__(
        self,
        cliente,
        servicio,
        duracion
    ):

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar_reserva(self):

        if self.duracion > 24:

            raise ServicioNoDisponibleError(
                "No se permiten reservas mayores a 24 horas"
            )

        costo = self.servicio.calcular_costo(
            self.duracion
        )

        self.estado = "Confirmada"

        registrar_log(
            f"Reserva confirmada: "
            f"{self.cliente.nombre}"
        )

        return costo


# ==============================
# SISTEMA PRINCIPAL
# ==============================

class SistemaReservas:

    def __init__(self):

        self.servicios = {

            "1": ReservaSala(
                "Sala de Conferencias",
                50
            ),

            "2": AlquilerEquipo(
                "Laptop High-End",
                20
            ),

            "3": AsesoriaEspecializada(
                "Consultoría Senior",
                100
            )
        }

    def mostrar_menu(self):

        print("\n" + "=" * 50)
        print("     SISTEMA DE RESERVAS")
        print("=" * 50)

        print("1. Sala de Conferencias")
        print("2. Laptop High-End")
        print("3. Consultoría Senior")

    def iniciar(self):

        try:

            self.mostrar_menu()

            nombre = input(
                "\nIngrese su nombre: "
            )

            email = input(
                "Ingrese su email: "
            )

            if not nombre or not email:

                raise DatosInvalidosError(
                    "Debe completar todos los campos"
                )

            opcion = input(
                "\nSeleccione un servicio (1-3): "
            )

            if opcion not in self.servicios:

                raise DatosInvalidosError(
                    "Servicio inválido"
                )

            duracion = float(
                input(
                    "Ingrese duración en horas: "
                )
            )

            servicio = self.servicios[opcion]

            cliente = Cliente(
                1,
                nombre,
                email
            )

            reserva = Reserva(
                cliente,
                servicio,
                duracion
            )

            costo = reserva.procesar_reserva()

            print("\n" + "=" * 50)
            print("        RESERVA EXITOSA")
            print("=" * 50)

            print(
                f"Cliente: {cliente.nombre}"
            )

            print(
                f"Email: {cliente.email}"
            )

            print(
                f"Servicio: "
                f"{servicio.nombre_servicio}"
            )

            print(
                f"Duración: "
                f"{duracion} horas"
            )

            print(
                f"Costo Total: "
                f"${costo:.2f}"
            )

            print(
                f"Estado: "
                f"{reserva.estado}"
            )

            print("=" * 50)

        except ValueError:

            print(
                "\nERROR: "
                "La duración debe ser numérica"
            )

        except SistemaError as e:

            registrar_log(str(e))

            print(
                f"\nERROR DEL SISTEMA: {e}"
            )

        except Exception as e:

            registrar_log(
                f"ERROR INESPERADO: {str(e)}"
            )

            print(
                f"\nOcurrió un error: {e}"
            )


# ==============================
# EJECUCIÓN
# ==============================

if __name__ == "__main__":

    sistema = SistemaReservas()

    sistema.iniciar()
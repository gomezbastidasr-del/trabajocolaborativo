import abc
import datetime


# =========================================
# FUNCION PARA REGISTRAR LOGS
# =========================================

def registrar_log(mensaje):

    with open("logs_sistema.txt", "a", encoding="utf-8") as archivo:

        fecha = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        archivo.write(f"[{fecha}] {mensaje}\n")


# =========================================
# EXCEPCIONES PERSONALIZADAS
# =========================================

class DatosInvalidosError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


class SistemaError(Exception):
    pass


# =========================================
# CLASE ABSTRACTA PERSONA
# =========================================

class Persona(abc.ABC):

    @abc.abstractmethod
    def obtener_descripcion(self):
        pass


# =========================================
# CLASE CLIENTE
# =========================================

class Cliente(Persona):

    def __init__(self, id_cliente, nombre, email):

        self.__id = id_cliente
        self.__nombre = nombre
        self.email = email

        registrar_log(f"Cliente creado: {nombre}")

    @property
    def nombre(self):

        return self.__nombre

    def obtener_descripcion(self):

        return f"Cliente: {self.__nombre} | ID: {self.__id}"


# =========================================
# CLASE ABSTRACTA SERVICIO
# =========================================

class Servicio(abc.ABC):

    def __init__(self, nombre_servicio, precio_base):

        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base

    @abc.abstractmethod
    def calcular_costo(self, duracion):
        pass


# =========================================
# CLASE RESERVA DE SALA
# =========================================

class ReservaSala(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:

            raise DatosInvalidosError(
                "La duración debe ser mayor a cero."
            )

        impuesto = 0.19

        total = (self.precio_base * duracion)

        return total + (total * impuesto)


# =========================================
# CLASE ALQUILER DE EQUIPOS
# =========================================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:

            raise DatosInvalidosError(
                "La duración debe ser mayor a cero."
            )

        descuento = 10

        total = (self.precio_base * duracion)

        return total - descuento


# =========================================
# CLASE ASESORIA ESPECIALIZADA
# =========================================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:

            raise DatosInvalidosError(
                "La duración debe ser mayor a cero."
            )

        return self.precio_base * duracion


# =========================================
# CLASE RESERVA
# =========================================

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar_reserva(self):

        try:

            print(f"\nProcesando reserva de {self.cliente.nombre}")

            if self.duracion > 24:

                raise ServicioNoDisponibleError(
                    "No se permiten reservas mayores a 24 horas."
                )

            # POLIMORFISMO
            costo = self.servicio.calcular_costo(
                self.duracion
            )

            self.estado = "Confirmada"

            print("Reserva realizada correctamente.")
            print(f"Costo total: ${costo:.2f}")

            registrar_log(
                f"Reserva confirmada para "
                f"{self.cliente.nombre}"
            )

        except (
            DatosInvalidosError,
            ServicioNoDisponibleError
        ) as error:

            self.estado = "Fallida"

            registrar_log(
                f"ERROR: {str(error)}"
            )

            raise SistemaError(
                "Error al procesar la reserva."
            )

        finally:

            print(
                f"Estado final: {self.estado}"
            )


# =========================================
# FUNCION PRINCIPAL
# =========================================

def ejecutar_sistema():

    print("===================================")
    print("   SISTEMA DE RESERVAS FJ")
    print("===================================")

    # SERVICIOS
    sala = ReservaSala(
        "Sala de Conferencias",
        50
    )

    equipo = AlquilerEquipo(
        "Laptop Gamer",
        20
    )

    asesoria = AsesoriaEspecializada(
        "Consultoría Senior",
        100
    )

    # ESCENARIOS
    operaciones = [

        ("Juan", sala, 5),
        ("Ana", equipo, 2),
        ("Pedro", asesoria, 30),
        ("Luis", sala, -1),
        ("Marta", equipo, 10)

    ]

    for nombre, servicio, horas in operaciones:

        try:

            cliente = Cliente(
                101,
                nombre,
                f"{nombre.lower()}@gmail.com"
            )

            reserva = Reserva(
                cliente,
                servicio,
                horas
            )

            reserva.procesar_reserva()

        except SistemaError as e:

            print(f"ERROR CONTROLADO: {e}")

        print("-" * 40)


# =========================================
# INICIO DEL PROGRAMA
# =========================================

if __name__ == "__main__":

    ejecutar_sistema()
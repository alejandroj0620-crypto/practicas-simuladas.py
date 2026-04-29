import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
import datetime

# ================== LOGGER ==================
class Logger:
    @staticmethod
    def log(mensaje):
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {mensaje}\n")


# ================== EXCEPCIONES ==================
class SistemaError(Exception):
    pass

class ClienteError(SistemaError):
    pass

class ServicioError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass


# ================== CLASE ABSTRACTA ==================
class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def mostrar(self):
        pass


# ================== CLIENTE ==================
class Cliente(Entidad):
    def __init__(self, id, nombre, email):
        super().__init__(id)
        if not nombre:
            raise ClienteError("Nombre inválido")
        if "@" not in email:
            raise ClienteError("Email inválido")

        self.__nombre = nombre
        self.__email = email

    def mostrar(self):
        return f"{self.__nombre} ({self.__email})"

    def get_nombre(self):
        return self.__nombre


# ============= SERVICIO ABSTRACTO ============
class Servicio(Entidad):
    def _init_(self, id, nombre, tarifa_base):
        super()._init_(id)

        if not nombre:
            raise ServicioError("Nombre de servicio inválido")
        if tarifa_base <= 0:
            raise ServicioError("Tarifa base inválida")

        self._nombre = nombre
        self._tarifa_base = tarifa_base

    def mostrar(self):
        return f"Servicio: {self._nombre} - Tarifa: {self._tarifa_base}"
        
    def convertir_a_horas(self, cantidad, unidad):
        try:
            if cantidad <= 0:
                raise ServicioError("Cantidad inválida")

            if unidad == "horas":
                return cantidad
            elif unidad == "dias":
                return cantidad * 24
            elif unidad == "semanas":
                return cantidad * 24 * 7
            else:
                raise ServicioError("Unidad de tiempo no válida")

        except Exception as e:
            Logger.log(f"Error al convertir tiempo: {str(e)}")
            raise ServicioError("Error en conversión de tiempo") from e

    # --------- MÉTODO ABSTRACTO ---------
    @abstractmethod
    def calcular_costo(self, cantidad, unidad):
        pass
# ================== SERVICIOS ==================
class ReservaSala(Servicio):
    def calcular_costo(self, cantidad, tipo):
        horas = self.convertir_tiempo(cantidad, tipo)
        return self.precio_base * horas


class AlquilerEquipo(Servicio):
    def calcular_costo(self, cantidad, tipo):
        horas = self.convertir_tiempo(cantidad, tipo)
        return self.precio_base * horas * 0.8


class Asesoria(Servicio):
    def calcular_costo(self, cantidad, tipo):
        horas = self.convertir_tiempo(cantidad, tipo)
        return self.precio_base * horas * 1.2

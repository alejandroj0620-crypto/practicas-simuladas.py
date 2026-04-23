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
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    def convertir_tiempo(self, cantidad, tipo):
        if tipo == "Horas":
            return cantidad
        elif tipo == "Días":
            return cantidad * 24
        elif tipo == "Semanas":
            return cantidad * 24 * 7
        else:
            raise ServicioError("Unidad de tiempo inválida")

    @abstractmethod
    def calcular_costo(self, cantidad, tipo):
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

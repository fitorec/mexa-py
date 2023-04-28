# encoding: utf-8
""" Se encarga de implementar funciones para el nucleo de la aplicacion. """
import re
import math
import datetime
from typing import Union


class Partes:
    """Se encarga de dividir el valor en partes"""

    def __init__(self, regex:str):
        """
        Constructor

        :param regex: expresion regular con la que trabajará
        :type regex: str

        """
        self.regex = regex
        self.error = True
        self.re_obj = None

    def load(self, value:str):
        """
        Carga el valor en el objeto evaluando dicho valor con el regex

        :param value: valor del elemento en cuestión.
        :type value: str

        """
        self.re_obj = re.search(self.regex, value)
        if self.re_obj:
            self.error = False
        else:
            self.error = True

    def get(self, index:str) -> Union[str, None]:
        """
        Devuelve un grupo dentro de la expresión regular

        :param index: el indice del grupo a devolver.
        :type index: int
        :return: El grupo en cuestion ó None en caso de error
        :rtype: str/None

        """
        if self.error:
            return None
        try:
            el = self.re_obj.group(index)
            return el
        except IndexError as e:
            print(f"Exeption: {e}")
            return None

    def value(self) -> Union[str, None]:
        """
        Devuelve un grupo 0 que contiene el valor empatado.
        :return: El grupo 0
        :rtype: str
        :rtype: str/None
        """
        return self.get(0)

class FieldInterface:
    """Forza a que la función que la implemente sobre-escriba los metodos vacios"""
    errors = []
    errorMsgs = {}

    @staticmethod
    def is_valid(value, match = None):
        """Devuelve true si value es valido"""
        pass


    @staticmethod
    def generate(data):
        """Devuelve el valor a partir de los metadatos recibidos en data"""
        pass


    @staticmethod
    def autocomplete(value):
        """Devuelve un string igual o mayor al recibido"""
        pass


    @classmethod
    def add_error(cls, code = 100, value = None):
        """Agrega el mensaje de error y devuelve siempre False"""
        msg = ''
        if code in cls.errorMsgs:
            msg = cls.errorMsgs[code]
            if value is not None:
                msg = msg.format(value)
        else:
            msg = f'Código de error incorrecto: {code}'
        cls.errors.append(msg)
        return False


    @classmethod
    def has_errors(cls):
        """Devuelve true si existen errores"""
        return len(cls.errors) > 0


    @classmethod
    def clear_errors(cls):
        """Recibe un mensaje y lo guarda en el error"""
        cls.errors.clear()


def year_by_last2digit (last2_digits):
    """
    Regresa el año completo a partir de los dos últimos digitos

    :param last2_digits: los dos últimos digitos del año, p.e. 23 para el 2023
    :type last2_digits: int
    :return: El año completo
    :rtype: int

    """
    y = int(last2_digits)
    if math.isnan(y):
        return None
    current_year = datetime.date.today().year % 100
    centenas = 20 if y <= current_year else 19
    return (centenas * 100) + y

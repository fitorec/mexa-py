# encoding: utf-8
''' Se encarga de implementar funciones para el nucleo de la aplicacion. '''
import math
import datetime


class FieldInterface:
    '''Forza a que la función que la implemente sobre-escriba los metodos vacios'''
    errors = []
    errorMsgs = {}

    @staticmethod
    def is_valid(value):
        '''Devuelve true si value es valido'''
        pass


    @staticmethod
    def generate(data):
        '''Devuelve el valor a partir de los metadatos recibidos en data'''
        pass


    @staticmethod
    def autocomplete(value):
        '''Devuelve un string igual o mayor al recibido'''
        pass


    @classmethod
    def add_error(cls, code = 100, value = None):
        '''Agrega el mensaje de error y devuelve siempre False'''
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
        '''Devuelve true si existen errores'''
        return len(cls.errors) > 0


    @classmethod
    def clear_errors(cls):
        '''Recibe un mensaje y lo guarda en el error'''
        cls.errors.clear()


def year_by_last2digit (last2_digits):
# def complete_year(last2digits):
    '''Regresa el año completo a partir de los dos últimos digitos'''
    y = int(last2_digits)
    if math.isnan(y):
        return None
    current_year = datetime.date.today().year % 100
    centenas = 20 if y <= current_year else 19
    return (centenas * 100) + y

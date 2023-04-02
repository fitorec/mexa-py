# encoding: utf-8
''' Se encarga de implementar funciones para el nucleo de la aplicacion. '''



class FieldInterface:
    '''Forza a que la función que la implemente sobre-escriba los metodos vacios'''
    error_msg = None
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

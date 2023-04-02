'''Mexa validador y generador de campos'''
from mexa.NssField import NssField

def fake(type_field, data):
    '''faker'''
    if type_field == 'nss':
        return NssField.generate(data)
    raise TypeError(f"Tipo invalido: {type_field}")

def validate(type_field, value):
    '''faker'''
    if type_field == 'nss':
        return NssField.is_valid(value)
    raise TypeError(f"Tipo invalido: {type_field}")

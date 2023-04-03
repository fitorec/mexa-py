'''Mexa validador y generador de campos'''
from mexa.NssField import NssField as NSS

def fake(type_field, data):
    '''faker'''
    if type_field == 'nss':
        return NSS.generate(data)
    raise TypeError(f"Tipo invalido: {type_field}")

def validate(type_field, value):
    '''faker'''
    if type_field == 'nss':
        return NSS.is_valid(value)
    raise TypeError(f"Tipo invalido: {type_field}")

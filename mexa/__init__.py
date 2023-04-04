'''Mexa validador y generador de campos'''
from mexa.NssField import NssField as NSS
from mexa.CurpField import CurpField as Curp

def fake(type_field, data):
    '''faker'''
    if type_field == 'nss':
        return NSS.generate(data)
    if type_field == 'curp':
        return Curp.generate(data)
    raise TypeError(f"Tipo invalido: {type_field}")

def validate(type_field, value):
    '''faker'''
    if type_field == 'nss':
        return NSS.is_valid(value)
    if type_field == 'curp':
        return Curp.is_valid(value)
    raise TypeError(f"Tipo invalido: {type_field}")

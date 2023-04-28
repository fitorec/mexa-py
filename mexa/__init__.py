"""Mexa validador y generador de campos"""
from mexa.NssField import NssField as Nss
from mexa.CurpField import CurpField as Curp, CurpTools


def generate(type_field, data):
    """genera a partir de los datos recibidos"""
    if type_field == 'nss':
        return Nss.generate(data)
    if type_field == 'curp':
        return Curp.generate(data)
    raise TypeError(f"Tipo invalido: {type_field}")

def fake(type_field):
    """faker"""
    return generate(type_field, {})

def validate(type_field, value, match = None):
    """Valida el type_field el valor"""
    if type_field == 'nss':
        return Nss.is_valid(value, match)
    if type_field == 'curp':
        return Curp.is_valid(value, match)
    raise TypeError(f"Tipo invalido: {type_field}")

__all__ = ['generate', 'validate', 'Curp', 'Nss', 'CurpTools']

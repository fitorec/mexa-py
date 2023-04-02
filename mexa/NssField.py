# encoding: utf-8
'''Clase encargada del NSS'''
import datetime
import re
import random
from mexa.core import FieldInterface

class NssField(FieldInterface):
    '''Clase que modela el NSS'''

    @staticmethod
    def nss_checksum(nss):
        '''Recibe una cadena de 10(o mas) caracteres y regresa el checksum de los primeros diez'''
        if len(nss) < 10:
            NssField.error_msg = None
            return -1
        suma = 0
        for i in range(10):
            factor = 2 if (i % 2 == 1) else 1
            v = int(nss[i]) * factor
            suma += (1 + v % 10) if (v >9) else v
        cs = (suma * 9) % 10
        return cs

    @staticmethod
    def complete_year(last2digits):
        '''Regresa el año completo a partir de los dos últimod digitos'''
        y = int(last2digits)
        current_year = datetime.date.today().year % 100
        centenas = 20 if y <= current_year else 19
        return (centenas * 100) + y

    @staticmethod
    def is_valid(value):
        '''Devuelve true si value es valido'''
        NssField.error_msg = None
        if len(value) != 11:
            NssField.error_msg = 'El valor debe tener una longitud de 11'
            return False
        s = re.search(r'^(\d{2})(\d{2})(\d{2})(\d{4})(\d)$', value)
        if not s:
            NssField.error_msg = 'Formato invalido de entrada'
            return False
        # reg_imss = s.group(1)
        f_afi = NssField.complete_year(s.group(2))
        f_nac = NssField.complete_year(s.group(3))
        if int(f_afi) < int(f_nac):
            NssField.error_msg = f"No se pudo afiliar({f_afi}) antes de haber nacido({f_nac})"
            return False
        if NssField.nss_checksum(value) == int(s.group(5)):
            return True
        NssField.error_msg = 'Input invalido'
        return False

    @staticmethod
    def autocomplete(value):
        '''Devuelve true si value es valido'''
        if len(value) != 10:
            return value
        cs = NssField.nss_checksum(value)
        return f"{value}{cs}"

    @staticmethod
    def anios(data  = None):
        '''Devuelve arreglo ordenado con los años de nacimeinto y el de afiliacion'''
        if data is None:
            data  = {}
        if 'f_nacimiento' in data and 'f_afiliacion' in data:
            return [
              NssField.complete_year(data['f_nacimiento']),
              NssField.complete_year(data['f_afiliacion'])
            ]
        if 'f_nacimiento' in data:
            nac = NssField.complete_year(data['f_nacimiento'])
            while True:
                afil = NssField.complete_year(random.randrange(0, 99))
                if afil >= nac:
                    return [nac, afil]
        if 'f_afiliacion' in data:
            afil  = NssField.complete_year(data['f_afiliacion'])
            while True:
                nac = NssField.complete_year(random.randrange(0, 99))
                if afil >= nac:
                    return [nac, afil]
        y1 = NssField.complete_year(random.randrange(0, 99))
        y2 = NssField.complete_year(random.randrange(0, 99))
        if y1 <= y2:
            return [y1, y2]
        return [y2, y1]

    @staticmethod
    def generate(data = None):
        '''Devuelve un NSS valido'''
        if data is None:
            data  = {}
        region_imss = data['region_imss'] if 'region_imss' in data else random.randrange(0, 99)
        years = NssField.anios(data)
        folio_imss = data['folio_imss'] if 'folio_imss' in data else random.randrange(10, 9999)
        # Variables a usar
        reg = str(region_imss).rjust(2, '0')
        afi = str(years[1])[-2:] # Año de Afiliacion
        nac = str(years[0])[-2:] # Año de Nacimiento
        fol = str(folio_imss).rjust(4, '0')
        return NssField.autocomplete(f'{reg}{afi}{nac}{fol}')

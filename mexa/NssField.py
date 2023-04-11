# encoding: utf-8
'''Clase encargada del Nss'''
import random
from mexa.core import FieldInterface, year_by_last2digit, Partes
from mexa.ErrorMsgs import NSS_ERRORS as ERRORS

partes = Partes(r'^(\d{2})(\d{2})(\d{2})(\d{4})(\d)$')
REGION_IMSS = 1
ANIO_ALTA = 2
ANIO_NACIMIENTO = 3
FOLIO_IMSS = 4
CHECKSUM = 5

class NssField(FieldInterface):
    '''Clase que modela el Nss'''
    errorMsgs = ERRORS
    # region_imss, anio_alta, anio_nacimiento, folio_imss, checksum

    @staticmethod
    def nss_checksum(nss):
        '''Recibe un string que representa el nss, regresa el checksum'''
        if len(nss) < 10:
            NssField.error_msg = None
            return -1
        suma = 0
        for i in range(10):
            factor = 1 + (i % 2)
            v = int(nss[i]) * factor
            suma += (1 + v % 10) if (v > 9) else v
        cs = (suma * 9) % 10
        return cs


    @staticmethod
    def is_valid(value, match = None):
        '''Devuelve true si value es valido'''
        NssField.clear_errors()
        if len(value) != 11:
            NssField.add_error(code = 100)
            return False
        partes.load(value)
        if partes.error:
            NssField.add_error(code = 100)
            return False
        # revisando los años de afiliación/nacimiento
        f_afi = year_by_last2digit(partes.get(ANIO_ALTA))
        f_nac = year_by_last2digit(partes.get(ANIO_NACIMIENTO))
        if int(f_afi) < int(f_nac):
            NssField.add_error(code = 101)
            return False
        # revisando el checksum
        cs = NssField.nss_checksum(value)
        if cs != int(partes.get(CHECKSUM)):
            NssField.add_error(code = 102, value = partes.get(CHECKSUM))
            return False
        # Falta agregar la implementación del match
        return match is None

    @staticmethod
    def autocomplete(value):
        '''Devuelve true si value es valido'''
        if len(value) != 10:
            return value
        cs = NssField.nss_checksum(value)
        return f"{value}{cs}"


    @staticmethod
    def anios(data  = None):
        '''
        Devuelve un arreglo con los años de nacimiento y afiliacion

        :param dic data: Los datos el cual puede contener fecha_nacimiento
                        y f_afiliacion de existir deberán ser tomados
                        en cuenta estos valores.
        :return: Arreglo ordenado de la forma [fecha_nacimiento, f_afiliacion]
        '''
        if data is None:
            data  = {}
        if 'fecha_nacimiento' in data and 'f_afiliacion' in data:
            return [
              year_by_last2digit(data['fecha_nacimiento']),
              year_by_last2digit(data['f_afiliacion'])
            ]
        if 'fecha_nacimiento' in data:
            nac = year_by_last2digit(data['fecha_nacimiento'])
            while True:
                afil = year_by_last2digit(random.randrange(0, 99))
                if afil >= nac:
                    return [nac, afil]
        if 'f_afiliacion' in data:
            afil  = year_by_last2digit(data['f_afiliacion'])
            while True:
                nac = year_by_last2digit(random.randrange(0, 99))
                if afil >= nac:
                    return [nac, afil]
        y1 = year_by_last2digit(random.randrange(0, 99))
        y2 = year_by_last2digit(random.randrange(0, 99))
        if y1 <= y2:
            return [y1, y2]
        return [y2, y1]


    @staticmethod
    def generate(data = None):
        '''
        Genera un Nss a partir de los datos recibidos.

        :param dic data: Los valores contenidos deberán ser tomados en cuenta.
        :return: str nss Un número del Seguro Social válido
        '''
        if data is None:
            data  = {}
        reg = data['region_imss'] if 'region_imss' in data else random.randrange(0, 99)
        years = NssField.anios(data)
        fol = data['folio_imss'] if 'folio_imss' in data else random.randrange(0, 9999)
        # Asignacion y formato
        reg = str(reg).rjust(2, '0')
        afi = str(years[1])[-2:] # Año de Afiliacion
        nac = str(years[0])[-2:] # Año de Nacimiento
        fol = str(fol).rjust(4, '0')
        # Se envia a autocomplete los diez primeros digitos para que le agregue el cs
        return NssField.autocomplete(f'{reg}{afi}{nac}{fol}')

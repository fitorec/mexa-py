# encoding: utf-8
'''Módulo que contiene un conjunto de utilerías diseñadas para darle soporte a la Clae CurpField'''
import datetime
import string
from random import randint
from calendar import monthrange
from mexa.Estados import estados

ALPHABET = string.ascii_uppercase
DIGITS = string.digits
VOWELS = "AEIOU"
CONSONANTS = [letter for letter in ALPHABET if letter not in VOWELS]

class Rand():
    '''Devuelve aleatoriamente diferentes elementos'''
    @staticmethod
    def digito():
        '''Regresa un valor aleatorio entre 0 a 9'''
        return str(randint(0, 9))


    @staticmethod
    def vocal():
        '''Regresa un valor aleatorio entre 0 a 9'''
        return VOWELS[randint(0, len(VOWELS) - 1)]


    @staticmethod
    def consonante():
        '''Regresa un valor aleatorio entre 0 a 9'''
        return CONSONANTS[randint(0, len(CONSONANTS) - 1)]


    @staticmethod
    def estado():
        '''Devuelve un estado aleatorio'''
        edos = estados.keys()
        return edos[randint(0, len(edos) - 1)]


    @staticmethod
    def fecha():
        '''Devuelve un estado aleatorio'''
        y_actual = datetime.date.today().year
        y = randint(y_actual - 80, y_actual - 10)
        m = randint(1, 12)
        dias_info = monthrange(y, m)
        d = randint(1, dias_info[1])
        return str(y)[2:4] + str(m).rjust(2, '0') + str(d).rjust(2, '0')


class CurpTools():
    '''Clase que modela el CURP'''
    @staticmethod
    def sanitizar(value):
        '''Sanitiza un string'''
        remplazos = {
            'A': ['Ã', 'À', 'Á', 'Ä', 'Â'],
            'E': ['È', 'É', 'Ë', 'Ê'],
            'I': ['Ì', 'Í', 'Ï', 'Î'],
            'O': ['Ò', 'Ó', 'Ö', 'Ô'],
            'U': ['Ù', 'Ú', 'Ü', 'Û'],
            'a': ['ã', 'à', 'á', 'ä', 'â'],
            'e': ['è', 'é', 'ë', 'ê'],
            'i': ['ì', 'í', 'ï', 'î'],
            'o': ['ò', 'ó', 'ö', 'ô'],
            'u': [ 'ù','ú', 'ü', 'û'],
            'C': ['Ç', 'ç'],
            'X': ['ñ', 'Ñ'],
        }
        out = ''
        keys = remplazos.keys()
        for char in value:
            insertado = False
            for key in keys:
                if char in remplazos[key]:
                    insertado = True
                    out += key
                    break
            if not insertado:
                out += char
        return out.upper()


    @staticmethod
    def primer_vocal_interna(value):
        '''Sanitiza un string'''
        if len(value) == 0:
            return 'X'
        for c in value[1:]:
            if c in ('A','E','I','O','U'):
                return c
        return 'X'


    @staticmethod
    def primer_consonante_interna(value):
        '''Sanitiza un string'''
        if len(value) == 0:
            return 'X'
        for c in value[1:]:
            if c not in ('A','E','I','O','U'):
                return c
        return 'X'


    @staticmethod
    def primer_letra(s):
        '''Sanitiza un string'''
        return s[0] if len(s) else 'X'


    # Cuando el nombre o los apellidos son compuestos y tienen
    # proposiciones, contracciones o conjunciones, se deben eliminar esas palabras
    # a la hora de calcular el CURP.
    @staticmethod
    def quitar_conjunciones(s):
        '''Devuelve el nombre de pila'''
        parts = CurpTools.sanitizar(s).split(' ')
        if len(parts) == 1:
            return parts[0]
        compuestos = (
            'DA', 'DAS', 'DE', 'DEL', 'DER', 'DI', 'DIE', 'DD', 'EL', 'LA',
            'LOS', 'LAS', 'LE', 'LES', 'MAC', 'MC', 'VAN', 'VON', 'Y'
        )
        out = ' '.join([e for e in parts if e not in compuestos])
        return s if out == '' else out


    @staticmethod
    def limpiar_mal_palabra(nombre):
        '''Quita una mala palabra'''
        malasPalabras = [
          'BACA', 'BAKA', 'BUEI', 'BUEY', 'CACA', 'CACO', 'CAGA', 'CAGO', 'CAKA',
          'CAKO', 'COGE', 'COGI', 'COJA', 'COJE', 'COJI', 'COJO', 'COLA', 'CULO',
          'FALO', 'FETO', 'GETA', 'GUEI', 'GUEY', 'JETA', 'JOTO', 'KACA', 'KACO',
          'KAGA', 'KAGO', 'KAKA', 'KAKO', 'KOGE', 'KOGI', 'KOJA', 'KOJE', 'KOJI',
          'KOJO', 'KOLA', 'KULO', 'LILO', 'LOCA', 'LOCO', 'LOKA', 'LOKO', 'MAME',
          'MAMO', 'MEAR', 'MEAS', 'MEON', 'MIAR', 'MION', 'MOCO', 'MOKO', 'MULA',
          'MULO', 'NACA', 'NACO', 'PEDA', 'PEDO', 'PENE', 'PIPI', 'PITO', 'POPO',
          'PUTA', 'PUTO', 'QULO', 'RATA', 'ROBA', 'ROBE', 'ROBO', 'RUIN', 'SENO',
          'TETA', 'VACA', 'VAGA', 'VAGO', 'VAKA', 'VUEI', 'VUEY', 'WUEI', 'WUEY'
        ]
        if nombre not in malasPalabras:
            return nombre
        return f'{nombre[0]}X{nombre[2:4]}'


    @staticmethod
    def nombre_de_pila(nombre):
        '''Devuelve el nombre de pila'''
        parts = CurpTools.quitar_conjunciones(nombre).split(' ')
        if len(parts) <= 1:
            return parts[0]
        especiales = ('JOSE', 'J.', 'MARIA', 'MA.')
        for p in parts:
            if p not in especiales:
                return p
        return parts[0] if len(parts) else 'X'

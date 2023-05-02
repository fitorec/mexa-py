# encoding: utf-8
"""
Módulo que contiene un conjunto de utilerías diseñadas
para darle soporte a la Clase: CurpField
"""
import re
import math
import datetime
import string
from random import randint, choice
from calendar import monthrange
from mexa.Estados import estados

ALPHABET = string.ascii_uppercase
DIGITS = string.digits
VOWELS = "AEIOU"
CONSONANTS = [letter for letter in ALPHABET if letter not in VOWELS]

class Rand():
    """Devuelve aleatoriamente diferentes elementos"""

    @staticmethod
    def digito():
        """Regresa un valor aleatorio entre 0 a 9


        :returns: i ∈ (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

        :rtype: int

        Example:

        >>> Rand.digito() # 3 (por ejemplo)
        """
        return str(randint(0, 9))


    @staticmethod
    def vocal():
        """Regresa una vocal aleatoriamente


        :returns: s ∈ (A, E, I, O , U)

        :rtype: str

        Example:

        >>> Rand.digito() # 3 (por ejemplo)
        """
        return choice(VOWELS)


    @staticmethod
    def consonante():
        """Devuelve una consonante de manera aleatoria.


        :returns: s ∈ ALPHABET) ^ (s ∉ VOWELS)

        :rtype: str

        Example:

        >>> Rand.consonante() # M (por ejemplo)
        """
        return choice(CONSONANTS)

    @staticmethod
    def sexo():
        """Devuelve el sexo en modo aleatorio


        :returns: s ∈ (H, M)

        :rtype: str

        Example:

        >>> Rand.sexo() # M (por ejemplo)
        """
        return choice(['H', 'M'])

    @staticmethod
    def estado():
        """Devuelve el código de un estado de forma aleatoria


        :returns: s ∈ ESTADOS_CODIGOS

        :rtype: str

        Example:

        >>> Rand.estado() # "MN" ("Michoacán de Ocampo",por ejemplo)
        """
        return choice(list(estados.keys()))


    @staticmethod
    def fecha() -> str:
        """Devuelve una fecha aleatoria en formato de 6 carácteres.


        :returns: AAMMDD

        :rtype: str

        Example:

        >>> Rand.fecha() # "200229" ("29/feb/2020", por ejemplo)
        """
        y_actual = datetime.date.today().year
        y = randint(y_actual - 80, y_actual - 10)
        m = randint(1, 12)
        dias_info = monthrange(y, m)
        d = randint(1, dias_info[1])
        return str(y)[2:4] + str(m).rjust(2, '0') + str(d).rjust(2, '0')


class CurpTools():
    """Clase que modela el CURP"""
    @staticmethod
    def sanitizar(value:str) -> str:
        """Recibe un string y devuelve su equivalente normalizado.

        :param value: valor del str a sanitizar.
        :type value: str
        :param value:str: 
        :returns: el str sanitizado.
        :rtype: str

        """
        remplazos = {
            'A': ['Ã', 'À', 'Á', 'Ä', 'Â', 'ã', 'à', 'á', 'ä', 'â'],
            'E': ['È', 'É', 'Ë', 'Ê', 'è', 'é', 'ë', 'ê'],
            'I': ['Ì', 'Í', 'Ï', 'Î', 'ì', 'í', 'ï', 'î'],
            'O': ['Ò', 'Ó', 'Ö', 'Ô', 'ò', 'ó', 'ö', 'ô'],
            'U': ['Ù', 'Ú', 'Ü', 'Û', 'ù', 'ú', 'ü', 'û'],
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
    def primer_vocal_interna(palabra:str) -> str:
        """Devuelve la primer vocal de parabra

        :param palabra: La palabra sobre en cual se buscará la primer vocal.
        :type palabra: str
        :param palabra:str: 
        :returns: La primer vocal interna encontrada, Si no encuentra devuelve X
        :rtype: str

        Example:

        >>> CurpTools.primer_vocal_interna('OLLA') # A
        >>> CurpTools.primer_vocal_interna('ELY')  # X (no encontró)
        """
        if len(palabra) == 0:
            return 'X'
        for c in palabra[1:]:
            if c in ('A','E','I','O','U'):
                return c
        return 'X'


    @staticmethod
    def primer_consonante_interna(palabra):
        """Devuelve el valor de la primer consonante interna en palabra

        :param palabra: palabra con la que se van a trabajar.
        :type palabra: str
        :returns: El valor de la primer consonante.
        :rtype: str

        Example:

        >>> CurpTools.primer_consonante_interna('JOEL') # L
        >>> CurpTools.primer_consonante_interna('TIO')  # X (No se encontró)
        """
        if len(palabra) == 0:
            return 'X'
        for c in palabra[1:]:
            if c not in ('A','E','I','O','U'):
                return c
        return 'X'


    @staticmethod
    def primer_letra(palabra: str) -> str:
        """Devuelve la primer letra de la palabra recibida.

        :param palabra: La parabra en la que se extrae el primer caracter.
        :type palabra: str
        :param palabra: str: 
        :returns: la primer letra en caso que la cadena es vacia regresa X
        :rtype: str

        Example:

        >>> CurpTools.primer_letra('JOEL')    # J
        >>> CurpTools.primer_letra('Miguel')  # M
        """
        return palabra[0] if len(palabra) else 'X'


    #
    #
    # a la hora de calcular el CURP.
    @staticmethod
    def quitar_conjunciones(s):
        """Cuando el nombre o los apellidos son compuestos y tienen proposiciones,
        contracciones o conjunciones, se deben eliminar esas palabras son eliminadas.

        :param s: string el cual se le quitaran las conjunciones.
        :type s: str
        :returns: El texto de entrada sin contracciones, conjunciones, etc..
        :rtype: str

        Example:

        >>> CurpTools.quitar_conjunciones("DE LA CRUZ") # "CRUZ"
        >>> CurpTools.quitar_conjunciones("DEL CUELLO DI ANGEL") # "CUELLO ANGEL"
        """
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
    def limpiar_mal_palabra(palabra:str) -> str:
        """Transforma una "mala palabra".

        :param palabra: Palabra a buscar si es "mala palabra".
        :type palabra: str
        :param palabra:str: 
        :returns: la palabra original en caso de ser "mala" la limpia.
        :rtype: str

        Example:

        >>> CurpTools.limpiar_mal_palabra("CACA") # "CXCA"
        >>> CurpTools.limpiar_mal_palabra("HOLA") # "HOLA" (sin cambio)
        >>> CurpTools.limpiar_mal_palabra("PITO") # "PXTO"
        """
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
        if palabra not in malasPalabras:
            return palabra
        return f'{palabra[0]}X{palabra[2:4]}'


    @staticmethod
    def nombre_de_pila(nombre:str) -> str:
        """Devuelve el nombre de pila, en donde si el primer nombre es María o
        José devolverá el segundo nombre.

        :param nombre: Nombre del que se sacará el nombre de pila
        :type nombre: str
        :param nombre:str: 
        :returns: Nombre de pila
        :rtype: str

        Example:

        >>> CurpTools.nombre_de_pila("JOSE ANGEL")   # "ANGEL"
        >>> CurpTools.nombre_de_pila("MA. FERNANDA") # "FERNANDA"
        >>> CurpTools.nombre_de_pila("JUAN ANGEL")   # "JUAN"
        >>> CurpTools.nombre_de_pila("J. DEL CIELO") # "CIELO"
        """
        parts = CurpTools.quitar_conjunciones(nombre).split(' ')
        if len(parts) <= 1:
            return parts[0]
        especiales = ('JOSE', 'J.', 'MARIA', 'MA.')
        for p in parts:
            if p not in especiales:
                return p
        return parts[0] if len(parts) else 'X'

    @staticmethod
    def anio(last2_digits:str, homo_serial:str) -> int:
        """Devuelve al año, agregando los primeros digitos, esto si la parte de la
        homoclave que genera la serialización para evitar curps repetidos Si es
        mayor a A entonces nacio despues del año 2000

        :param last2_digits: Los dos ultimos digitos del año.
        :type last2_digits: str
        :param homo_serial: Valor de la homoclave
        :type homo_serial: str
        :param last2_digits:str: 
        :param homo_serial:str: 
        :returns: El año obtenido.
        :rtype: int

        Example:

        >>> CurpTools.anio("20", "0") # 1920
        >>> CurpTools.anio("20", "A") # 2020
        """
        y = int(last2_digits)
        if math.isnan(y):
            return None
        centenas = 19 if homo_serial in "01234566789" else 20
        return (centenas * 100) + y

    @staticmethod
    def fecha_to_6digits(fecha) -> str:
        """Recibe una fecha y la normaliza a formato AAMMDD

        :param fecha: La fecha
        :returns: La fecha en formato AAMMDD
        :rtype: str

        """
        if isinstance(fecha, datetime.date):
            fecha = fecha.strftime("%Y-%m-%d")
        if not isinstance(fecha, str):
            return None
        if re.match(r'^\d{6}$', fecha):
            return fecha
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            return None
        return f'{fecha[2:4]}{fecha[5:7]}{fecha[8:10]}'

    @staticmethod
    def estado_to_2chars(edo):
        """Recibe el estado devuelve el código del mismo a dos caracteres

        :param edo: El nombre del estado
        :type edo: str
        :returns: El codigo del estado
        :rtype: str

        """
        if len(edo) != 2:
            try:
                index = list(estados.values()).index(edo)
                edo = list(estados.keys())[index]  # Prints george
            except ValueError:
                return None
        return edo

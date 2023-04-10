# encoding: utf-8
'''Clase encargada del CURP'''
import re
from random import randint
from calendar import monthrange
from mexa.core import FieldInterface, year_by_last2digit
from mexa.Estados import estados
from mexa.CurpUtils import Rand, CurpTools, CONSONANTS
from mexa.ErrorMsgs import CURP_ERRORS

class CurpField(FieldInterface):
    '''CurpField'''
    errorMsgs = CURP_ERRORS

    @staticmethod
    def gen_id_nombre(data):
        '''Genera la parte del nombre, los primeros 4 dígitos'''
        out = ['X','X','X','X']
        # Tomando la parte del primer apellido (paterno)
        if 'primer_ap' in data:
            primer_ap = CurpTools.quitar_conjunciones(data['primer_ap'])
            out[0] = CurpTools.primer_letra(primer_ap)
            out[1] = CurpTools.primer_vocal_interna(primer_ap)
        else:
            out[0] = Rand.consonante()
            out[1] = Rand.vocal()
        # Tomando la parte del segundo apellido (materno)
        if 'segundo_ap' in data:
            segundo_ap = CurpTools.quitar_conjunciones(data['segundo_ap'])
            out[2] = CurpTools.primer_letra(segundo_ap)
        else:
            out[2] = Rand.consonante()
        # Tomando la parte del nombre
        if 'nombre' in data:
            nombre = CurpTools.nombre_de_pila(data['nombre'])
            out[3] = CurpTools.primer_letra(nombre)
        else:
            out[3] = Rand.consonante()
        return CurpTools.limpiar_mal_palabra(''.join(out))


    @staticmethod
    def gen_id2_nombre(data):
        '''Genera la parte del nombre, los primeros 4 dígitos'''
        out = ['X','X','X']
        # Tomando la parte del primer apellido (paterno)
        if 'primer_ap' in data:
            primer_ap = CurpTools.quitar_conjunciones(data['primer_ap'])
            out[0] = CurpTools.primer_consonante_interna(primer_ap)
        else:
            out[0] = Rand.consonante()
        # Tomando la parte del segundo apellido (materno)
        if 'segundo_ap' in data:
            segundo_ap = CurpTools.quitar_conjunciones(data['segundo_ap'])
            out[1] = CurpTools.primer_consonante_interna(segundo_ap)
        else:
            out[1] =  Rand.consonante()
        # Tomando la parte del nombre
        if 'nombre' in data:
            nombre = CurpTools.nombre_de_pila(data['nombre'])
            out[2] = CurpTools.primer_consonante_interna(nombre)
        else:
            out[2] = Rand.consonante()
        return CurpTools.sanitizar(''.join(out))


    @staticmethod
    def error_parte_nombre1(s):
        '''Recibe la primer parte del nombre y valida esta'''
        print('parametro recibido:' + s)
        return False

    @staticmethod
    def error_parte_fecha(fecha_str):
        '''Revisa si existe algún error en el en formato fecha AAMMDD

            devuelve el código de error o
            None en caso de no existir error.
        '''
        y = year_by_last2digit(fecha_str[0:2])
        m = int(fecha_str[2:4])
        if m > 12:
            return 102
        dias_mes = monthrange(y, m)[1]
        d = int(fecha_str[4:6])
        if d > dias_mes:
            return 103
        return None

    @staticmethod
    def checksum(curp: str) -> int:
        """
        Calculate the checksum for the mexican CURP.
        """
        chars = "0123456789ABCDEFGHIJKLMNNOPQRSTUVWXYZ"
        suma = sum([(18 - i) * chars.index(curp[i]) for i in range(17)])
        return (10 - (suma % 10)) % 10

    @staticmethod
    def is_valid(value):
        '''Regresa True si y solo si value es un CURP valido'''
        # formato: id_nombre, f_nac, sexo, ent fed, id2_nombre, homoclave
        CurpField.clear_errors()
        # rex = r'^([A-Z]{4})(\d{6})([H|M])([A-Z]{2})([A-Z]{3})([A-Z0-9]{2})$'
        rex = r'^([A-Z]{4})(\d{6})([H|M])([A-Z]{2})([A-Z]{3})(\S)(\d)$'
        s = re.search(rex, CurpTools.sanitizar(value))
        if not s:
            CurpField.add_error(code = 100)
            return False
        # Fecha de nacimiento.
        error_code = CurpField.error_parte_fecha(s.group(2))
        if error_code is not None:
            CurpField.add_error(error_code)
        # Sexo
        if s.group(3) not in ('H', 'M'):
            CurpField.add_error(code = 101, value = s.group(3))
        # Entidad Federativa, NE es no especificado el caso común es para extrangeros
        # Ya que no nació en ninguna entidad federativa.
        if s.group(4) not in estados:
            CurpField.add_error(code = 104, value = s.group(4))
        # La parte del nombre esta conformada por la 1er consonante interna del:
        # primer apellido, 2d apellido, nombre pila
        par_nombre = s.group(5)
        for c in par_nombre:
            if c not in CONSONANTS:
                CurpField.add_error(code = 105, value = c)
        curp_val = s.group(0)
        cs = CurpField.checksum(curp_val)
        if cs != int(s.group(7)):
            CurpField.add_error(code = 106, value = curp_val)
        return not CurpField.has_errors()


    @staticmethod
    def gen_fecha_nacimiento(data):
        '''Genera la fecha de nacimiento'''
        if 'f_nacimiento' in data and len(data['f_nacimiento']) == 6:
            return data['f_nacimiento']
        return Rand.fecha()


    @staticmethod
    def gen_sexo(data):
        '''Genera el sexo'''
        if 'sexo' in data:
            if data['sexo'] in ('HOMBRE', 'MASCULINO', 'H'):
                return 'H'
            if data['sexo'] in ('MUJER', 'FEMENINO', 'F', 'M'):
                return 'M'
        index = randint(0, 9) % 2
        return ['H', 'M'][index]

    @staticmethod
    def gen_entidad_federativa(data):
        '''Genera el sexo'''
        if 'entidad_federativa' in data:
            return data['entidad_federativa']
        return 'OC'


    @staticmethod
    def generate(data):
        '''Devuelve el valor a partir de los metadatos recibidos en data'''
        id_nombre = CurpField.gen_id_nombre(data)
        fecha = CurpField.gen_fecha_nacimiento(data)
        sexo = CurpField.gen_sexo(data)
        ent_fed = CurpField.gen_entidad_federativa(data)
        id2_nombre = CurpField.gen_id2_nombre(data)
        # Generando el curp y su suma de verificación (cs).
        curp = f'{id_nombre}{fecha}{sexo}{ent_fed}{id2_nombre}0'
        cs = str(CurpField.checksum(curp))
        return f'{curp}{cs}'

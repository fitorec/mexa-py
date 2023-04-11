# encoding: utf-8
'''Clase encargada del CURP'''
from calendar import monthrange
from mexa.core import FieldInterface, Partes
from mexa.Estados import estados
from mexa.CurpUtils import Rand, CurpTools, CONSONANTS
from mexa.ErrorMsgs import CURP_ERRORS as ERRORS


# Expresión regular para validar y las partes(groups) que conforman el CURP
partes = Partes(r'^([A-Z]{4})(\d{6})([H|M])([A-Z]{2})([A-Z]{3})(\S)(\d)$')
ID_NOMBRE = 1
FECHA_NACIMIENTO = 2
SEXO = 3
ENTIDAD_FEDERATIVA = 4
ID2_NOMBRE = 5
HOMOCLAVE = 6
CHECKSUM = 7

class CurpField(FieldInterface):
    '''CurpField'''
    errorMsgs = ERRORS

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
    def check_fecha(fecha_str, homo_serial):
        '''Revisa si existe algún error en el en formato fecha AAMMDD

            devuelve el código de error o
            None en caso de no existir error.
        '''
        y = CurpTools.anio(fecha_str[0:2], homo_serial)
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
    def find_match_error_nombre(nombre, curp):
        '''Valida si para el nombre el curp es correcto'''
        if curp[3] != CurpTools.primer_letra(nombre):
            CurpField.add_error(201)
        if curp[15] != CurpTools.primer_consonante_interna(nombre):
            CurpField.add_error(202)

    @staticmethod
    def find_match_error_primer_ap(primer_ap, curp):
        '''Valida si para el primer apellido el curp es correcto'''
        if curp[0] != CurpTools.primer_letra(primer_ap):
            CurpField.add_error(203)
        if curp[1] != CurpTools.primer_vocal_interna(primer_ap):
            CurpField.add_error(204)
        if curp[10] != CurpTools.primer_consonante_interna(primer_ap):
            CurpField.add_error(205)

    @staticmethod
    def find_match_error_segundo_ap(segundo_ap, curp):
        '''Valida si para el primer apellido el curp es correcto'''
        if curp[2] != CurpTools.primer_letra(segundo_ap):
            CurpField.add_error(206)
        if curp[14] != CurpTools.primer_consonante_interna(segundo_ap):
            CurpField.add_error(207)

    @staticmethod
    def find_match_error(match):
        '''Devuelve el código de error en el match'''
        curp = partes.value()
        if 'nombre' in match:
            nombre = CurpTools.nombre_de_pila(CurpTools.sanitizar(match['nombre']))
            CurpField.find_match_error_nombre(nombre, curp)
        if 'primer_ap' in match:
            primer_ap = CurpTools.quitar_conjunciones(match['primer_ap'])
            CurpField.find_match_error_primer_ap(primer_ap, curp)
        if 'segundo_ap' in match:
            segundo_ap = CurpTools.quitar_conjunciones(match['segundo_ap'])
            CurpField.find_match_error_segundo_ap(segundo_ap, curp)
        if 'fecha_nacimiento' in match:
            fecha6digits = CurpTools.fecha_to_6digits(match['fecha_nacimiento'])
            if partes.get(FECHA_NACIMIENTO) != fecha6digits:
                CurpField.add_error(code = 208, value = match['fecha_nacimiento'])
        if 'sexo' in match:
            if partes.get(SEXO) != match['sexo']:
                CurpField.add_error(code = 209, value = match['sexo'])
        if 'entidad_federativa' in match:
            edo2chars = CurpTools.estado_to_2chars(match['entidad_federativa'])
            if partes.get(ENTIDAD_FEDERATIVA) != edo2chars:
                CurpField.add_error(code = 210, value = match['entidad_federativa'])

    @staticmethod
    def is_valid(value, match = None):
        '''Regresa True si y solo si value es un CURP valido'''
        CurpField.clear_errors()
        #
        partes.load(CurpTools.sanitizar(value))
        if partes.error:
            CurpField.add_error(code = 100)
            return False
        # Fecha de nacimiento.
        error_code = CurpField.check_fecha(
            partes.get(FECHA_NACIMIENTO),
            partes.get(HOMOCLAVE)
        )
        if error_code is not None:
            CurpField.add_error(error_code)
        # Sexo
        if partes.get(SEXO) not in ('H', 'M'):
            CurpField.add_error(code = 101, value = partes.get(SEXO))
        # Entidad Federativa, NE es no especificado el caso común es para extrangeros
        # Ya que no nació en ninguna entidad federativa.
        if partes.get(ENTIDAD_FEDERATIVA) not in estados:
            CurpField.add_error(code = 104, value = partes.get(ENTIDAD_FEDERATIVA))
        # La parte del nombre esta conformada por la 1er consonante interna del:
        # primer apellido, 2d apellido, nombre pila
        par_nombre = partes.get(ID2_NOMBRE)
        for c in par_nombre:
            if c not in CONSONANTS:
                CurpField.add_error(code = 105, value = c)
        curp_val = partes.value()
        # Valida el match.
        if  match is not None:
            # Falta agregar la implementación del match
            code = CurpField.find_match_error(match)
            if code is not None:
                CurpField.add_error(code)
            # CurpField.add_error(code = 100)
        # Checksum
        cs = CurpField.checksum(curp_val)
        if cs != int(partes.get(CHECKSUM)):
            CurpField.add_error(code = 106, value = curp_val)
        return not CurpField.has_errors()

    @staticmethod
    def gen_fecha_nacimiento(data):
        '''Genera la fecha de nacimiento'''
        if 'fecha_nacimiento' in data and len(data['fecha_nacimiento']) == 6:
            return data['fecha_nacimiento']
        return Rand.fecha()


    @staticmethod
    def gen_sexo(data):
        '''Genera el sexo'''
        if 'sexo' in data:
            if data['sexo'] in ('HOMBRE', 'MASCULINO', 'H'):
                return 'H'
            if data['sexo'] in ('MUJER', 'FEMENINO', 'F', 'M'):
                return 'M'
        return Rand.sexo()

    @staticmethod
    def gen_entidad_federativa(data):
        '''Genera el sexo'''
        if 'entidad_federativa' in data:
            return data['entidad_federativa']
        return Rand.estado()


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

# encoding: utf-8
"""Clase encargada del CURP"""
from calendar import monthrange
from mexa.core import FieldInterface, Partes
from mexa.Estados import estados
from mexa.CurpUtils import Rand, CurpTools, CONSONANTS
from mexa.ErrorMsgs import CURP_ERRORS as ERRORS


# Expresión regular para validar y las partes(groups) que conforman el CURP
partes = Partes(r'^([A-Z]{4})(\d{6})([H|M])([A-Z]{2})([A-Z]{3})(\S)(\d)$')
FECHA_NACIMIENTO = 2
SEXO = 3
ENTIDAD_FEDERATIVA = 4
ID2_NOMBRE = 5
HOMOCLAVE = 6
CHECKSUM = 7

class CurpField(FieldInterface):
    """
    CurpField, clase encargada de administrar el CURP, el cual lo representamos como:

    >>> #    ⌐------------------------------ id_nombre: 1ras letras 1er ap, 2do ap y nombre
    >>> #    |      ⌐----------------------- fecha_nacimiento: 6 digitos en orden AAMMDD
    >>> #    |      |    ⌐------------------ sexo: un carácter el cual puede ser H ó  M
    >>> #    |      |    |   ⌐-------------- entidad_federativa: codigo de 2 caracteres
    >>> #    |      |    |   |   ⌐---------- consonantes_internas: 1er ap, 2d ap y nombre
    >>> #    |      |    |   |   |    ⌐----- homoclave: Evita duplicidades
    >>> #    |      |    |   |   |    |  ⌐-- checksum: Digito verificador de integridad
    >>> #    |      |    |   |   |    |  |
    >>> #  NNNN  AAMMDD  S  EN  CCC   H  C
    >>> #  0123  012345  0  01  012   0  0
    """

    errorMsgs = ERRORS

    @staticmethod
    def gen_id_nombre(data):
        """
        Genera la parte del nombre, los primeros 4 dígitos,

        :param data: diccionario de datos a utilizar.
        :type data: dict
        :return: Genera el id del nombre un str de 4 carácteres.
        :rtype: str

        """
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
    def gen_consonantes_nombre(data):
        """
        Genera la segunda parte parte del nombre

        :param data: diccionario de datos a utilizar.
        :type data: dict
        :return: la segunda parte del nombre, en formato de 3 consonantes.
        :rtype: str

        """
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
        """
        Revisa si existe algún error en el en formato fecha AAMMDD

        :param fecha_str: Fecha en 6 digitos en formato AAMMDD
        :type fecha_str: str
        :return: devuelve el código de error o None en caso de no existir error.
        :rtype: CodeError/None

        """
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
        Calcula el checksum del CURP.

        :param curp: El curp sobre al cual se calcula el checksum.
        :type curp: str
        :return: el valor del checksum.
        :rtype: int

        """
        chars = "0123456789ABCDEFGHIJKLMNNOPQRSTUVWXYZ"
        suma = sum([(18 - i) * chars.index(curp[i]) for i in range(17)])
        return (10 - (suma % 10)) % 10


    @staticmethod
    def find_match_error_nombre(nombre:str, curp:str) -> str:
        """
        Valida si el curp para el nombre el curp es correcto

        :param nombre: Nombre a validar
        :type nombre: str
        :param curp: CURP a validar.
        :return: True si encontró algun error/False en caso contrario
        :rtype: bool

        """
        has_error = False
        if curp[3] != CurpTools.primer_letra(nombre):
            CurpField.add_error(201)
            has_error = True
        if curp[15] != CurpTools.primer_consonante_interna(nombre):
            CurpField.add_error(202)
            has_error = True
        return has_error

    @staticmethod
    def find_match_error_primer_ap(primer_ap:str, curp:str) -> bool:
        """
        Valida si para el primer apellido el curp es correcto

        :param primer_ap: El valor del primer apellido.
        :type primer_ap: str
        :param curp: El valor del CURP.
        :type curp: str
        :return: True si existe(n) error(es)/ False caso contrario
        :rtype: bool

        """
        has_error = False
        if curp[0] != CurpTools.primer_letra(primer_ap):
            has_error = True
            CurpField.add_error(203)
        if curp[1] != CurpTools.primer_vocal_interna(primer_ap):
            has_error = True
            CurpField.add_error(204)
        if curp[10] != CurpTools.primer_consonante_interna(primer_ap):
            has_error = True
            CurpField.add_error(205)
        return has_error

    @staticmethod
    def find_match_error_segundo_ap(segundo_ap:str, curp:str) -> bool:
        """
        Valida si para el primer apellido el curp es correcto

        :param segundo_ap: Valor del segundo apellido.
        :type segundo_ap: str
        :param curp: Valor del CURP
        :type curp: str
        :return: True si existe(n) error(es)/ False caso contrario
        :rtype: bool

        """
        if curp[2] != CurpTools.primer_letra(segundo_ap):
            CurpField.add_error(206)
        if curp[14] != CurpTools.primer_consonante_interna(segundo_ap):
            CurpField.add_error(207)

    @staticmethod
    def find_match_error(match:dict):
        """
        Busca errores a partir del match proporcionado.

        :param match: Diccionario de datos el cual puede contener los valores de nombre,
            primer_ap, segundo_ap, fecha_nacimiento, sexo y entidad_federativa
        :type match: dict

        """
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
        """
        Valida el CURP

        :param value: Contiene el valor del CURP.
        :type value: str
        :return: Regresa True si value es un CURP valido
        :rtype: bool

        """
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
    def gen_fecha_nacimiento(data:dict) -> str:
        """
        Genera/Busca la fecha de nacimiento

        :param data: Diccionario que puede contener el valor de fecha_nacimiento
        :type data: dic
        :return: Una fecha de nacimiento valida en forma de 6 digítos AAMMDD
        :rtype: str

        """
        if 'fecha_nacimiento' in data and len(data['fecha_nacimiento']) == 6:
            return data['fecha_nacimiento']
        return Rand.fecha()


    @staticmethod
    def gen_sexo(data:dict) -> str:
        """
        Genera el sexo, en caso de ya venir uno devuelve este normalizado.

        :param data: Diccionario de datos de parametros definidos por el usuario
        :type data: dict
        :return: El sexo un caracter que puede ser H ó M
        :rtype: str

        """
        if 'sexo' in data:
            if data['sexo'] in ('HOMBRE', 'MASCULINO', 'H'):
                return 'H'
            if data['sexo'] in ('MUJER', 'FEMENINO', 'F', 'M'):
                return 'M'
        return Rand.sexo()

    @staticmethod
    def gen_entidad_federativa(data:dict) -> str:
        """
        Genera la entidad federativa, en caso de ya venir uno devuelve esta.

        :param data: Diccionario de datos de parametros definidos por el usuario
        :type data: dict
        :return: La entidad_federativa un código de 2 carácteres
        :rtype: str

        """
        if 'entidad_federativa' in data:
            return data['entidad_federativa']
        return Rand.estado()


    @staticmethod
    def generate(data:dict) -> str:
        """
        Genera el CURP, en caso de ya venir uno devuelve esta.

        :param data: Diccionario de datos de parametros definidos por el usuario
        :type data: dict
        :return: el CURP código de 18 carácteres
        :rtype: str

        """
        id_nombre = CurpField.gen_id_nombre(data)
        fecha = CurpField.gen_fecha_nacimiento(data)
        sexo = CurpField.gen_sexo(data)
        ent_fed = CurpField.gen_entidad_federativa(data)
        id2_nombre = CurpField.gen_consonantes_nombre(data)
        # Generando el curp y su suma de verificación (cs).
        curp = f'{id_nombre}{fecha}{sexo}{ent_fed}{id2_nombre}0'
        cs = str(CurpField.checksum(curp))
        return f'{curp}{cs}'

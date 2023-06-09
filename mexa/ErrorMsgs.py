"""Contiene todos los mensajes de error"""

# Errores para el NSS
NSS_ERRORS = {
    100 : 'El valor debe tener una longitud de 11 carácteres númericos',
    101 : 'El año de afiliación no puede ser menor que el de nacimiento',
    102 : 'Suma de validación incorrecta({})',
}

# Errores del CURP
CURP_ERRORS = {
    100 : 'Valor en formato inválido',
    101 : 'El sexo debe ser H o M, valor invalido: {}',
    102 : 'Mes incorrecto',
    103 : 'La cantidad de días que supera a los del mes indicado.',
    104 : 'El codigo de entidad federativa({}) es inválido.',
    105 : 'Carácter ({}) invalido en la segunda parte del nombre.',
    106 : 'Suma de validación incorrecta ({}).',
    # match error
    201: 'La primer letra del nombre de pila debe ir en la posición 4',
    202: 'La primer consonante interna del nombre de pila debe ir en la posición 16',
    203: 'La primer letra del primer apellido debe ir en la posición 1',
    204: 'La primer vocal interna del primer apellido debe ir en la posición 2',
    205: 'La primer consonante interna del primer apellido debe ir en la posición 11',
    206: 'La primer letra del segundo apellido debe ir en la posición 3',
    207: 'La primer consonante interna del segundo apellido debe ir en la posición 15',
    208: 'Las fecha del Curp con el valor recibido({}) a validar',
    209: 'El sexo del CURP no coincide con el valor recibido({}) a validar',
    210: 'La entidad federativa del Curp no coincide con el valor recibido({})',
}

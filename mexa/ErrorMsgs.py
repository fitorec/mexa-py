'''Contiene todos los mensajes de error'''

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
    106 : 'Suma de validación incorrecta ({}).'
}

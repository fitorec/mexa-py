'''Pruebas unitarias sobre el CURP'''
from mexa import fake, validate, Curp
from test_data import curps as ejemplos


def test_sanitizar():
    '''Test Sanitizar'''
    assert Curp.sanitizar('PÉREZ') == 'PEREZ'
    assert Curp.sanitizar('Pingüino') == 'PINGUINO'
    assert Curp.sanitizar('piña') == 'PIXA'
    print("\n\ttest_sanitizar")

def test_nombre_de_pila():
    '''Test nombre_de_pila'''
    assert Curp.nombre_de_pila('ELIAS MIGUEL') == 'ELIAS'
    assert Curp.nombre_de_pila('MARIA IRENE') == 'IRENE'
    assert Curp.nombre_de_pila('JOSE LUIS') == 'LUIS'
    assert Curp.nombre_de_pila('JESUS EDUARDO') == 'JESUS'
    assert Curp.nombre_de_pila('MARIA DE LOURDES') == 'LOURDES'
    assert Curp.nombre_de_pila('JOSE MARIA') == 'JOSE'
    assert Curp.nombre_de_pila('MARIA JOSE') == 'MARIA'
    print("\ttest_nombre_de_pila")

def test_malas_palabras():
    '''Test nombre_de_pila'''
    assert Curp.limpiar_mal_palabra('CACA') == 'CXCA'
    assert Curp.limpiar_mal_palabra('PITO') == 'PXTO'
    assert Curp.limpiar_mal_palabra('PUTA') == 'PXTA'
    assert Curp.limpiar_mal_palabra('BUEY') == 'BXEY'
    assert Curp.limpiar_mal_palabra('VAGO') == 'VXGO'
    assert Curp.limpiar_mal_palabra('WUEY') == 'WXEY'
    print("\ttest_malas_palabras")

def test_is_valid():
    '''Revisa la funcion validate para la opción curp'''
    i = 0
    for c in ejemplos.data:
        is_valid = validate('curp', c['curp'])
        assert is_valid
        i += 1
        if not is_valid:
            print('\nError', c)
            break
    print(f"\ttest_is_valid, validando {i} CURPs")

def test_fake():
    '''Validando fake curps generadas'''
    i = 0
    for c in ejemplos.data:
        curp = fake('curp', c)
        assert validate('curp', curp)
        i += 1
    print(f"\ttest_fake, Generando {i} CURPs validos")

def test_gen_id_nombre():
    '''Valida la generación del nombre'''
    num_test = 0
    for c in ejemplos.data:
        id_nombre = Curp.gen_id_nombre(c)
        id_esperado = c['curp'][0:4]
        num_test += 1
        if not id_nombre == id_esperado:
            print('Numero de prueba', num_test)
            print('\nError', c, id_nombre)
            # break
        assert id_nombre == id_esperado
        #
        id2 = Curp.gen_id2_nombre(c)
        id2_esperado = c['curp'][13:16]
        if not id2 == id2_esperado:
            print(c)
            print('Numero de prueba', num_test)
            print('\nError', c)
            # break
        assert id2 == id2_esperado
        curp = Curp.generate(c)
        assert Curp.is_valid(curp)
    # print(Curp.error_msg)

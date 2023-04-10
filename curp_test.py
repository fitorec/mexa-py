'''Pruebas unitarias sobre el CURP'''
from mexa import fake, validate, generate, Curp, CurpTools
# .sanitizar(''.join(out))
from test_data import curps as ejemplos
from test_data import curps_simples


def test_sanitizar():
    '''Test Sanitizar'''
    assert CurpTools.sanitizar('PÉREZ') == 'PEREZ'
    assert CurpTools.sanitizar('Pingüino') == 'PINGUINO'
    assert CurpTools.sanitizar('piña') == 'PIXA'
    print("\n\ttest_sanitizar")


#def test_nombre_de_pila():
#    '''Test nombre_de_pila'''
#    assert Curp.nombre_de_pila('ELIAS MIGUEL') == 'ELIAS'
#    assert Curp.nombre_de_pila('MARIA IRENE') == 'IRENE'
#    assert Curp.nombre_de_pila('JOSE LUIS') == 'LUIS'
#    assert Curp.nombre_de_pila('JESUS EDUARDO') == 'JESUS'
#    assert Curp.nombre_de_pila('MARIA DE LOURDES') == 'LOURDES'
#    assert Curp.nombre_de_pila('JOSE MARIA') == 'JOSE'
#    assert Curp.nombre_de_pila('MARIA JOSE') == 'MARIA'
#    print("\ttest_nombre_de_pila")


#def test_malas_palabras():
#    '''Test nombre_de_pila'''
#    assert Curp.limpiar_mal_palabra('CACA') == 'CXCA'
#    assert Curp.limpiar_mal_palabra('PITO') == 'PXTO'
#    assert Curp.limpiar_mal_palabra('PUTA') == 'PXTA'
#    assert Curp.limpiar_mal_palabra('BUEY') == 'BXEY'
#    assert Curp.limpiar_mal_palabra('VAGO') == 'VXGO'
#    assert Curp.limpiar_mal_palabra('WUEY') == 'WXEY'
#    print("\ttest_malas_palabras")

def test_checksum():
    # curp: SABC560626MDFLRN09 <- 9 checksum(digito verificador).
    # cs = Curp.checksum('SABC560626MDFLRN09')
    # assert cs == '9'
    # curp: SABC560626MDFLRN09 <- 9 checksum(digito verificador).
    cs = Curp.checksum('AOLB851003MOCMPT01')
    assert str(cs) == '1'
    #
    cs = Curp.checksum('MAMM830609HOCRRG01')
    assert str(cs) == '1'

def test_is_valid():
    '''Revisa la funcion validate para la opción curp'''
    i = 0
    max = ['0', '']
    for c in ejemplos.data:
        is_valid = validate('curp', c['curp'])
        assert is_valid
        i += 1
        if not is_valid:
            print('\nError', c)
            break
    print(f"\ttest_is_valid, Fueron vvalidados {i} CURPs")

def test_checksum():
    '''Revisa la funcion validate para la opción curp'''
    i = 0
    for c in curps_simples.data:
        is_valid = validate('curp', c)
        assert is_valid
        if not is_valid:
            break
        cs = Curp.checksum(c)
        lastChar = str(c[len(c) - 1])
        assert int(lastChar) == cs
        i += 1
    print(f"\ttest_checksum, Fueron validados {i} checksums de CURPs")

def test_fake():
    '''Validando fake curps generadas'''
    for i in range(100):
        curp = fake('curp')
        assert validate('curp', curp)
        lastChar = str(curp[len(curp) - 1])
        homo = str(curp[len(curp) - 2])
        if lastChar != '0' and homo != '0':
            print(f'Curp con cs diferente de cero {curp}')
    print(f"\ttest_fake, Generando {i} CURPs validos")

def test_validate():
    '''Validando generate curps generadas'''
    # La cantidad de días(30) supera el máximo(28)
    assert not validate('curp', 'AAMR780230MGRBRN00')
    print(Curp.errors)
    # Mes (23) incorrecto
    assert not validate('curp', 'AAMR832301MGRBRN00')
    print(Curp.errors)
    print(f"\ttest_validate")

def test_generate():
    '''Validando generate curps generadas'''
    i = 0
    for c in ejemplos.data:
        curp = generate('curp', c)
        assert validate('curp', curp)
        i += 1
    print(f"\tgenerate, Generando {i} CURPs validos")

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
        if not Curp.is_valid(curp):
            print(f'CURP invalido {curp}, Errores:')
            print(Curp.has_errors())
            print(Curp.errors)
            # Curp.errors.clear()
            # print(Curp.errors())
            break
        assert Curp.is_valid(curp)
    # print(Curp.error_msg)

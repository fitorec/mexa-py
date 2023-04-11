''' Pruebas unitarias sobre el NSS '''
from mexa import fake, validate, Nss


def test_cien_intentos_case():
    '''realiza la validacion de 100 casos'''
    for i in range(100):
        nss = fake('nss')
        is_valid = validate('nss', nss)
        assert is_valid
        if not is_valid:
            print(f'Error en el NSS incorrecto {nss}, iteración {i}')
            break
    print("Se probaron la generación de 100 registros")

def test_caso_fallido():
    '''Pruebas en casos fallidos'''
    assert not validate('nss', '12345678901')
    print(Nss.errors[0])

def _test_validate_con_match():
    '''Realiza la validación a partir del match recibido'''
    #nss_data = {
    #    "region_imss" : "72",
    #    "folio_imss" : "0804",
    #    "f_nacimiento": "56",
    #    "f_afiliacion": "79",
    #}
    # assert  validate('nss', value = "BAUM690216HMSLRG18", match = match)

# def test_capital_case():
#    assert capital_case('semaphore') == 'Semaphore'

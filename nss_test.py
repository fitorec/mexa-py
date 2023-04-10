from mexa import fake, validate, Nss


def test_diez_intentos_case():
    for i in range(100):
        nss = fake('nss')
        print(nss)
        assert validate('nss', nss)
    print("Se probaron la generación de 100 registros")

def test_caso_fallido():
    assert not validate('nss', '12345678901')
    print(Nss.errors)


# def test_capital_case():
#    assert capital_case('semaphore') == 'Semaphore'

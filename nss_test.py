from mexa import fake, validate, NSS
# print("mexa.fake", fake('nss', {}))


def test_diez_intentos_case():
    for i in range(10):
        nss = fake('nss', {})
        print(nss)
        assert validate('nss', nss)

def test_caso_fallido():
    assert not validate('nss', '12345678901')
    print(NSS.error_msg)


# def test_capital_case():
#    assert capital_case('semaphore') == 'Semaphore'

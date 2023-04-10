<h1>
<span style="color:green">M</span>ex<span style="color:red">a</span>
<small>__Mexican Power__</small>
</h1>


#### Generador y Verificador de campos.

__Mexa__ es un validador y generador de diferentes campos, utiles para la tramitología mexicana:

### Listado de campos:

 - **CURP**: Clave Única de Registro de Población.
 - **Nss**: Número de Seguro Social.
 - **RFC**: Registro Federal de Contribuyentes(física y moral).
 - **Tel**: Telefonos con lada MX.



### Uso:



```python
from mexa import fake, validate, Nss, Curp

# Usando el comando fake para genearar un Nss completamente aleatorio.
nss = fake('nss') # Valor valido por ejemplo `48979152914`
if validate('nss', nss): # Esto debe valer True por lo tanto mostrará el nss generado
    print(nss)
#
curp = fake('curp') # Valor valido por ejemplo `AAMR740524HOCBRN08`
if validate('curp', curp): # Esto debe valer True
    print(curp)



# Un caso de error en donde el año de afiliación/nacimiento
if not validate('nss', '12345678901'):
    print(Nss.errors)

# De forma similar probamos con un valor invalido para el curp
if not validate('curp', '--invalido--'):
    print(Curp.errors)
#
```

### Instalación.


El paquete esta disponible en **pypi** (__<https://pypi.org/project/mexa/>__), para puedes instalarlo desde `pip`:

```
# Instalación de Mexa.
pip install mexa
```


# Número de seguro social Nss

El numero de seguro social de México se conforma de 11 dígitos:

## Formato.

El **Nss** esta conformado de las siguientes partes:


![Formato img](https://raw.githubusercontent.com/gist/fitorec/82a3e27fae3bab709a07c19c71c3a8d4/raw/0e545684368cbe536e001e3d7e8a1fe015036748/nss_checksum.svg)

### Diez digitos de información.

 - 2 Dígitos Región IMSS.
 - 2 Dígitos Año afiliación al Seguro Social.
 - 2 Dígitos Año de nacimiento.
 - 4 Folio IMSS.

### Un digito verificador (el último)

En la onceava posición y ultima posición se encuentra el dígito permite validar los diez dígitos previos, previniendo errores de captura pues la simple alteración de un digito en la cadena de diez digitos genera un cambio en el dígito verificador.

Este digito es creado por medio de una implementación del **algoritmo Luhn**.


> Nota: para mayores informes consultar la definición del algoritmo en wikipedia:
> :point_right:  <https://es.wikipedia.org/wiki/Algoritmo_de_Luhn>


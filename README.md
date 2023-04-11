<h1>
<span style="color:green">M</span>ex<span style="color:red">a</span> -
<small>Mexican Power</small>
</h1>


#### Generador y Verificador de campos.

__Mexa__ es un validador y generador de diferentes campos, utiles para la tramitología mexicana:

### Listado de campos:

 - **CURP**: Clave Única de Registro de Población.
 - **Nss**: Número de Seguro Social.
 - **RFC**: Registro Federal de Contribuyentes(física y moral).
 - **Tel**: Télefonos con lada de México.

### Instalación.


El paquete esta disponible en **pypi** (__<https://pypi.org/project/mexa/>__), para puedes instalarlo desde `pip`:

```
# Instalación de Mexa.
pip install mexa
```


### Uso:



```python
from mexa import fake, validate, Nss, Curp, generate


# ------------------------- fake --------------------------------------------
## Fake generando campos aleatorios.
#
nss = fake('nss') # Valor valido por ejemplo `48979152914`
curp = fake('curp') # Valor valido por ejemplo `AAMR740524HOCBRN08`

# ------------------------- validate ------------------------------------------
## Validación de datos
if validate('nss', nss): # Esto debe valer True por lo tanto mostrará el nss generado
    print(nss)

if validate('curp', curp): # Esto debe valer True
    print(curp)

## EXPERIMENTAL. #####
# Devuelve true si:
#  - El curp es valido
#  - Con el  valor del campo nombre, es viable formar el CURP recibido.
data = {"nombre" : "MIGUEL ANGEL"}
if validate('curp', value = "BAUM690216HMSLRG18", match = data):
    print(curp)

# ------------------------- generate ------------------------------------------
#
# Puede generar un curp tomando en consideración los datos que ingrese.
curp_str = generate('curp', data)
print('curp generada a partir del nombre', curp_str) # por ejemplo: ZUVM471127HOCTJG03
# Los datos restantes los genera de forma aleatoria, en este sentido es parecida a fake.
# Pero... en la medida que agregue datos el CURP generado es predictivo, ejemplo:
data = {
    "nombre" : "Juan Manuel",
    "primer_ap": "Lopéz",
    "segundo_ap": "Lopéz",
    "fecha_nacimiento": "780609", # 9 de junio del 1978
    "sexo": "H", # H: hombre, M: Mujer,
    "entidad_federativa": "SP" # San Luis Potosí
}
curp_str = generate('curp', data) # resultado: LOLJ780609HSPPPN09
print('curp generado con todos los datos recibidos', curp_str)

nss_data = {
    "region_imss" : "72",
    "folio_imss" : "0804",
    "fecha_nacimiento": "56",
    "f_afiliacion": "79",
}
nss_str = generate('nss', nss_data) # resultado: 72795608040
print('NSS generado con todos los datos recibidos', nss_str)

# ------------------------- Manejo de errores ---------------------------------

# Un caso de error en donde el año de afiliación/nacimiento
if not validate('nss', '12345678901'):
    print('NSS Errores: ', Nss.errors)

# De forma similar probamos con un valor invalido para el curp
if not validate('curp', '--invalido--'):
    print('CURP Errores: ', Curp.errors)
#

#
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


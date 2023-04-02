# Mexa Generador y Verificador de campos __Mexican Power__.

## Validación y generación de campos.



# Número de seguro social NSS 

El numero de seguro social de México se conforma de 11 dígitos:

## Formato.

El **NSS** esta conformado de las siguientes partes:


![Formato img](https://raw.githubusercontent.com/gist/fitorec/82a3e27fae3bab709a07c19c71c3a8d4/raw/0e545684368cbe536e001e3d7e8a1fe015036748/nss_checksum.svg)

### Diez digitos de información.

 - 2 Dígitos Región IMSS.
 - 2 Dígitos Año afiliación al Seguro Social.
 - 2 Dígitos Año de nacimiento.
 - 4 Folio IMSS.

### El verificador es el último dígito (el onceavo).

Este dígito permite validar los primeros diez dígitos previos, previniendo errores de captura pues la simple alteración de un digito en la cadena de diez digitos genera un cambio en el dígito verificador.

Este digito es creado por medio de una implementación del **algoritmo Luhn**.


> Nota: para mayores informes consultar la definición del algoritmo en wikipedia:
> :point_right:  <https://es.wikipedia.org/wiki/Algoritmo_de_Luhn>


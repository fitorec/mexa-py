.. meta::
   :description: Mexa Generador, Validador de campos para tramitologia Mexicana
   :keywords: Mexa, curp, nss, clabe, rfc, checksum, validador, faker



.. |github_link| raw:: html

    <a href="https://github.com/fitorec/mexa-py">Ver en GitHub</a>


Teoría sobre el CURP
==================================

El **CURP** (*Clave Única de Registro de Población*) es un documento de identificación personal en México que se utiliza para una amplia gama de propósitos oficiales, incluyendo la educación, la salud, el empleo y el registro de votantes.

Usos tipicos del **CURP** son:
----------------------------------------------------

El **CURP** es una herramienta importante para la identificación y registro de las personas en México, y es necesario para acceder a una amplia variedad de servicios y trámites oficiales, algunos de sus usos tipicos son:


 - **Identificación personal**: identificar a las personas de manera única y evitar la duplicación de registros.
 - **Trámites oficiales**: realizar diversos trámites oficiales, como la obtención de una licencia de conducir, la inscripción en la escuela, el registro de una empresa, entre otros.
 - **Registro de votantes**: Es un requisito para registrarse como votante en México.
 - **Servicios de salud**: para acceder a servicios de salud del gobierno, como el Seguro Popular y el IMSS.
 - **Control migratorio**: Es utilizado para controlar la migración en el territorio mexicano.




Estructura del CURP
----------------------------------------------------

.. _imagen-ejemplo:

   .. figure:: /_static/chabelo_curp.png
      :alt: Curp de ejemplo caso Chabelo
      :figclass: figure
      :align: center

      Descripción detallada de una CURP de ejemplo. Caso Chabelo.

.. note::
   La imagen muestra el curp de **Xavier Lopéz Rodríguez** quien nació en el extrangero, por lo tanto el valor en Entidad Federativa es ``NE`` *No especificado*.


- **id_nombre**: formada de los siguientes 4 caracteres
   - Primera letra del primer apellido.
   - Primera vocal del primer apellido.
   - Primera letra del segundo apellido (en caso de tenerlo).
   - Primera letra del nombre de pila.
- **fecha_nacimiento**: 6 digitos conformados de la siguiente manera AAMMDD:
   - Dos dígitos correspondientes al año de nacimiento.
   - Dos dígitos correspondientes al mes de nacimiento.
   - Dos dígitos correspondientes al día de nacimiento.
- **Sexo**: Una letra para indicar el sexo (H para hombre y M para mujer).
- **entidad_federativa** Código de dos letras que identifican la entidad federativa de nacimiento.
- **consonantes_internas** Segundo identificador del nombre, conformado por
   - Primer consonante interna del 1er apellido
   - Primer consonante interna del 2do apellido
   - Primer consonante interna del Nombre de pila
- **homoclave**: Garantiza la unicidad de la clave, siendo un "`número`" serial, este tiene la caracteristica que para los que nacieron antes del año 2000 inicia con 0, mientras que los que nacieron del 2000 en adelante una A.
- **checksum:** Digito verificador de los 17 caracteres previos, el calculo de este hace una variante del `algoritmo Luhn <https://es.wikipedia.org/wiki/Algoritmo_de_Luhn>`_.

:ref:  imagen_ejemplo

.. code-block:: shell

   #   ⌐------------------------------ id_nombre: 1ras letras 1er ap, 2do ap y nombre
   #   |      ⌐----------------------- fecha_nacimiento: 6 digitos en orden AAMMDD
   #   |      |    ⌐------------------ sexo: un carácter el cual puede ser H ó  M
   #   |      |    |   ⌐-------------- entidad_federativa: codigo de 2 caracteres
   #   |      |    |   |   ⌐---------- consonantes_internas: 1er ap, 2d ap y nombre
   #   |      |    |   |   |    ⌐----- homoclave: Evita duplicidades
   #   |      |    |   |   |    |  ⌐-- checksum: Digito verificador de integridad
   #   |      |    |   |   |    |  |
   # NNNN  AAMMDD  S  EN  CCC   H  C
   # 0123  012345  0  01  012   0  0

Código de Entidad Federativa:
---------------------------------------------
Los caracteres en la posición ``11`` y ``12`` en la `imagen de ejemplo <#imagen-ejemplo>`_ se encuentrán dados por un código de dos caracteres que corresponden a la entidad federativa de nacimiento, estos códigos se enecuentran dados por la siguiente tabla:

.. csv-table:: Cátalogo de Entidades Federativas
   :file: ./csv/catalogo_entidades_federativas.csv
   :widths: 30, 70
   :header-rows: 1

.. note::
  `Diario Oficial de la Federación, Fecha: 23/10/1996 - Edición Matutina <https://dof.gob.mx/index_111.php?year=1996&month=10&day=23#gsc.tab=0>`_. Ejemplar Completo(*PDF*) P8 **CLAVES DE ENTIDADES FEDERATIVAS**

.. note::
  Puede consultar en linea el Catalo de Entidades Oficial: http://www.dgis.salud.gob.mx/contenidos/intercambio/entidades_gobmx.html

Checksum
-------------------------------------------

.. admonition:: Como se calcula el checksum?

   Usa una variante del `algoritmo Luhn <https://es.wikipedia.org/wiki/Algoritmo_de_Luhn>`_


.. csv-table:: Tabla de Equivalencias de Carácteres
   :file: ./csv/tabla_caracteres_curp.csv
   :widths: 25, 25, 25, 25
   :header-rows: 1

**Ejemplo**: para el curp **LORX350217HNEPDV08** en el cual claramente el checksum deberá ser **8**:

 - **Asignar indice descendiente** (*decreciente*): tal que para **L** es ``18``, **O** 17, **R** 16 y asi sucesivamente asta llegar al **0** con ``2``.
 - **Asignar el valor equivalente a cada caracter**: A cada carácter se le asigna el valor correspondiente en la tabla, para **L** le corresponde ``21``, **O**  ``25``, asi sucesivamente asta llegar al **0** con ``0``.
 - **Multiplicar el indice por el valor equivalente**: A cada caracter se le multiplica el indice por su valor equivalente en la tabla, **L** con indice ``18`` y valor equivalente ``21`` que tendrá como producto ``18*21 = 378``.


.. csv-table:: Tabla de ejemplo Caso LORX350217HNEPDV08
   :file: ./csv/ejemplo_tabla_checksum.csv
   :widths: 10, 25, 25, 40
   :header-rows: 1


Posteriormente se suman los productos de cada indice con su valor correspondiente, somo se muestra a continuación:

.. math::

   \sum_{indice=18}^2 suma = {indice} • {valor} = 378 + 425 + ... + 96 + 0 = {2,622}

Lo cual seria ``suma = 378 + 425 + ... + 0`` el cual para este ejemplo nos da el valor de **2,622**.

La formula del **checksum** en función de la variable **suma** esta representada por la siguiente expresión:

.. math::

    checksum = 10 - (suma \% 10)

.. note::
   Donde la operación **%** (*módulo*) representa el residuo de la división, en este caso de **suma** entre ``10`` lo cual lo convierte en un caso particular donde tiene la *función* de extraer el **último digito** de **suma**.

   **Por ejemplo**: Para ``suma = 2,622`` la operación es ``2,622 % 10 = residuo(2,622 / 10) = 2``, para ``suma = 2,623`` la operación es ``2,623 % 10 = residuo(2,623 / 10) = 3`` y asi sucesivamente va a extraer el útimo numero por ejemplo para ``suma = 1,999`` la operación es ``1,999 % 10 = residuo(1,999 / 10) = 9``.

De la formula anterior al remplazar **suma** por su valor obtenido previamente tras realizar la sumatoria el cual es **2,622** quedando como:

.. math::

   checksum  = 10 - (suma \% 10) =  10 - (2,622 \% 10) =  10 - (2) = 8


El cual nos devuelve el valor esperado de **8**, queda al lector realizar alguna otra prueba.

.. note::
   Usted puede validar dicho CURP `En el sitio Oficial del Gobierno de México <https://www.gob.mx/curp/>`_.


Enlaces relacionados
-------------------------------------------

 - `Clase CurpField <mexa.html#mexa.CurpField.CurpField>`_.


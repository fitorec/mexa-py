.. meta::
   :description: Mexa Generador, Validador de campos para tramitologia Mexicana
   :keywords: Mexa, curp, nss, clabe, rfc, checksum, validador, faker



.. |github_link| raw:: html

    <a href="https://github.com/fitorec/mexa-py">Ver en GitHub</a>




Documentación Mexa
==================================

.. image:: /_static/mexa_banner.png
   :alt: Mexa Banner
   :align: center


Instalación y Ejemplo:
======================

Para facilitar el uso el paquete esta `disponible en PyPi <https://pypi.org/project/mexa/>`_ por lo cual una forma simple de acceder el paquete es desde **pip**:

.. code-block:: shell

    pip install mexa

Una vez instalado el paquete lo puedes usar importandolo como cualquier paquete de python, por ejemplo:

.. code-block:: python

   from mexa import fake, validate, Nss, Curp, generate

   # Generando datos
   nss = fake('nss') # Número de Seguro social válido por ejemplo `48979152914`
   curp = fake('curp') # CURP válido por ejemplo `AAMR850214MGRBRN01`

   # Validando datos
   # Caso especial el de "Chabelo" que nacio en el extrangero
   # Por lo cual su entidad federativa es "NE" (No especificada)
   curp_especial = 'LORX350217HNEPDV08'
   validate('curp', value = curp_especial) # True
   # Los valores generados previamente por fake deberían ser correctos
   validate('nss', value = nss) # True
   validate('curp', value = curp) # True

Lista de módulos disponibles
============================================

.. toctree::
   :maxdepth: 4
   :caption: Estructura de módulos:


   modules

#   mexa

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

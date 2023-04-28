.. |github_link| raw:: html

    <a href="https://github.com/fitorec/mexa-py">Ver en GitHub</a>


.. sidebar:: Navigation

   * |github_link|
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`


Documentación Mexa
==================================

.. image:: /_static/mexa_banner.png
   :alt: Mexa Banner
   :align: center

Instalación y Ejemplo:
======================

Debes instalar antes el paquete:

.. code-block:: shell

    pip install mexa

Una vez instalado el paquete lo puedes usar importandolo como cualquier paquete de python, por ejemplo:

.. code-block:: python

   from mexa import fake, validate, Nss, Curp, generate
   nss = fake('nss') # Valor valido por ejemplo `48979152914`

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

from setuptools import setup

readme = open('./README.md', 'r')

setup(
    name = 'mexa',
    version = '0.6',
    packages=['mexa'],
    description = 'Validador y Generador de campos para tramites mexicanos',
    author='@Fitorec - Miguel Angel Marcial Martinez',
    author_email = 'fitorec@mundosica.com',
    url = 'https://github.com/fitorec/mexa-py',
    long_description = readme.read(),
    long_description_content_type = 'text/markdown',
    keywords = [
        'RFC', 'CURP', 'NSS', 'Clabe'
    ],
    classifiers = [
        'Programming Language :: Python :: 3.8',
    ],
    license = "MIT",
    include_package_data=True
)

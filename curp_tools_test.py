"""Pruebas unitarias sobre el CURP"""
from mexa import CurpTools


def test_primer_vocal_interna():
    """Test Sanitizar"""
    assert CurpTools.primer_vocal_interna("OLLA") == "A"
    assert CurpTools.primer_vocal_interna("ELY") == "X"
    assert CurpTools.primer_vocal_interna("MIGUEL") == "I"


def test_primer_consonante_interna():
    """Test Sanitizar"""
    assert CurpTools.primer_consonante_interna("JOEL") == "L"
    assert CurpTools.primer_consonante_interna("TIO") == "X" # (No se encontró)
    assert CurpTools.primer_consonante_interna("MIGUEL") == "G"



def test_quitar_conjunciones():
    """Test Sanitizar"""
    assert CurpTools.quitar_conjunciones("DE LA CRUZ") == "CRUZ"
    assert CurpTools.quitar_conjunciones("DEL CUELLO DI ANGEL") == "CUELLO ANGEL"
    # assert CurpTools.primer_consonante_interna("TIO") == "X" # (No se encontró)
    # assert CurpTools.primer_consonante_interna("MIGUEL") == "G"


def test_limpiar_mal_palabra():
    """Test limpiar_mal_palabra"""
    assert CurpTools.limpiar_mal_palabra("BUEY") == "BXEY"
    assert CurpTools.limpiar_mal_palabra("CACA") == "CXCA"
    assert CurpTools.limpiar_mal_palabra("HOLA") == "HOLA" # (sin cambio)
    assert CurpTools.limpiar_mal_palabra("PITO") == "PXTO"


def test_nombre_de_pila():
    """Test nombre_de_pila"""
    assert CurpTools.nombre_de_pila("JOSE ANGEL") == 'ANGEL'
    assert CurpTools.nombre_de_pila("MA. FERNANDA") == 'FERNANDA'
    assert CurpTools.nombre_de_pila("JUAN ANGEL") == 'JUAN'
    assert CurpTools.nombre_de_pila("J. DEL CIELO") == 'CIELO'


def test_anio():
    """Test nombre_de_pila"""
    assert CurpTools.anio("20", "0") == 1920
    assert CurpTools.anio("20", "A") == 2020

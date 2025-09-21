# app/calculadora.py
"""Módulo de funciones matemáticas básicas."""


def sumar(a, b):
    """Suma dos números."""
    return a + b


def restar(a, b):
    """Resta dos números."""
    return a - b


def multiplicar(a, b):
    """Multiplica dos números."""
    return a * b


def dividir(a, b):
    """Divide dos números."""
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b


def modulo(a, b):
    """Calcula el módulo de dos números."""
    mensaje = "No se puede calcular el módulo con divisor cero"

    if b == 0:
        raise ZeroDivisionError(mensaje)
    return a % b


def potencia(a, b):
    """Calcula a elevado a la b."""
    return a**b

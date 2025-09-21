# app/app.py
"""Aplicación web de calculadora usando Flask."""

import os
from flask import Flask, render_template, request
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField


from .calculadora import sumar, restar, multiplicar, dividir, modulo, potencia

app = Flask(__name__)
app_port = int(os.environ.get("PORT", 5000))
app.secret_key = os.getenv("CSRF_KEY", "")
csrf = CSRFProtect(app)


class FormCalculadora(FlaskForm):
    """form simple con CSRF."""

    num1 = StringField("num1")
    num2 = StringField("num2")
    operacion = StringField("operacion")


@app.route("/health")
def health():
    """Endpoint de salud"""
    return "OK", 200


@app.route("/calcular", methods=["POST"])
@app.route("/", methods=["GET"])
def index():
    """Página principal de la calculadora."""
    resultado = None
    form = FormCalculadora()
    if request.method == "POST":
        try:
            num1 = float(form.num1.data or "")
            num2 = float(form.num2.data or "")
            operacion = form.operacion.data

            if operacion == "sumar":
                resultado = sumar(num1, num2)
            elif operacion == "restar":
                resultado = restar(num1, num2)
            elif operacion == "multiplicar":
                resultado = multiplicar(num1, num2)
            elif operacion == "dividir":
                resultado = dividir(num1, num2)
            elif operacion == "modulo":
                resultado = modulo(num1, num2)
            elif operacion == "potencia":
                resultado = potencia(num1, num2)
            else:
                resultado = "Operación no válida"
        except ValueError:
            resultado = "Error: Introduce números válidos"
        except ZeroDivisionError:
            resultado = "Error: No se puede dividir por cero"

    return render_template("index.html", resultado=resultado, form=form)


if __name__ == "__main__":  # pragma: no cover
    app.run(port=app_port, host="0.0.0.0")

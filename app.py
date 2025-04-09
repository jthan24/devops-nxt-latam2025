from random import randint
from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/lanzardado")
def roll_dice():
    jugador = request.args.get('jugador', default=None, type=str)
    resultado = str(lanzar())
    if jugador:
        logger.warning("El jugador %s lanzo el dado: %s", jugador, resultado)
    else:
        logger.warning("Jugador Anonimo lanzo el dado: %s", resultado)
    return resultado


def lanzar():
    return randint(1, 6)
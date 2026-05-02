from flask import Blueprint

from src.controllers.template_controller import alive

template_bp = Blueprint("template", __name__)

template_bp.route("/alive", methods=["GET"])(alive)

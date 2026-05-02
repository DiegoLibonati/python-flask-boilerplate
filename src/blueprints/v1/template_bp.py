from flask import Blueprint

from src.controllers.template_controller import alive, test_error

template_bp = Blueprint("template", __name__)

template_bp.route("/alive", methods=["GET"])(alive)
template_bp.route("/test_error", methods=["GET"])(test_error)

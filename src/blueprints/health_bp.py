from flask import Blueprint, jsonify

from src.constants.codes import CODE_SUCCESS_HEALTH, CODE_SUCCESS_READY
from src.constants.messages import MESSAGE_SUCCESS_HEALTH, MESSAGE_SUCCESS_READY

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"code": CODE_SUCCESS_HEALTH, "message": MESSAGE_SUCCESS_HEALTH}), 200


@health_bp.route("/ready", methods=["GET"])
def ready():
    return jsonify({"code": CODE_SUCCESS_READY, "message": MESSAGE_SUCCESS_READY}), 200

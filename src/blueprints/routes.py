from flask import Flask

from src.blueprints.v1.template_bp import template_bp


def register_routes(app: Flask) -> None:
    prefix = "/api/v1"

    app.register_blueprint(template_bp, url_prefix=f"{prefix}/templates")

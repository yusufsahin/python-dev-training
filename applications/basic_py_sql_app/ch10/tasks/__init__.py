from __future__ import annotations

import os

import click
from flask import Flask

from tasks.blueprints.main import bp as tasks_bp
from tasks.config import Config
from tasks.extensions import csrf
from tasks.mongo import init_mongo


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    root = os.path.dirname(os.path.abspath(__file__))
    app.static_folder = os.path.join(root, "static")
    app.template_folder = os.path.join(root, "templates")

    app.config.from_object(config_class)
    csrf.init_app(app)
    init_mongo(app)

    app.register_blueprint(tasks_bp)

    @app.cli.command("seed-demo")
    def seed_demo_cmd() -> None:
        from tasks.seed import seed_demo_data

        seed_demo_data()

    @app.cli.command("ensure-initial-data")
    def ensure_initial_data() -> None:
        from tasks.models import Task
        from tasks.seed import seed_demo_data

        if Task.objects.count() > 0:
            click.echo("Seed skipped: database already has tasks.")
            return
        click.echo("Running initial seed…")
        seed_demo_data()
        click.echo("Initial data ready.")

    return app

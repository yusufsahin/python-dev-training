from __future__ import annotations

import os

import click
from flask import Flask
from sqlalchemy import func, select

from tasks.blueprints.main import bp as tasks_bp
from tasks.config import Config, resolve_database_uri
from tasks.extensions import csrf, db, migrate


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    root = os.path.dirname(os.path.abspath(__file__))
    app.static_folder = os.path.join(root, "static")
    app.template_folder = os.path.join(root, "templates")

    app.config.from_object(config_class)
    app.config["SQLALCHEMY_DATABASE_URI"] = resolve_database_uri(app)

    db.init_app(app)
    migrations_dir = os.path.join(os.path.dirname(app.root_path), "migrations")
    migrate.init_app(app, db, directory=migrations_dir)
    csrf.init_app(app)

    app.register_blueprint(tasks_bp)

    @app.cli.command("seed-demo")
    def seed_demo_cmd() -> None:
        from tasks.seed import seed_demo_data

        seed_demo_data()

    @app.cli.command("ensure-initial-data")
    def ensure_initial_data() -> None:
        """Seed demo tasks only when the database has no rows."""
        from tasks.models import Task
        from tasks.seed import seed_demo_data

        n = db.session.scalar(select(func.count()).select_from(Task))
        if n and n > 0:
            click.echo("Seed skipped: database already has tasks.")
            return
        click.echo("Running initial seed…")
        seed_demo_data()
        click.echo("Initial data ready.")

    return app

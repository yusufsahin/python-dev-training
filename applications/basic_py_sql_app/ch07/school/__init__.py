from __future__ import annotations

import click
from flask import Flask, redirect, request
from sqlalchemy import func, select
from whitenoise import WhiteNoise

from school.blueprints.api import bp as api_bp
from school.blueprints.main import bp as school_bp
from school.config import Config, static_dir
from school.extensions import csrf, db, migrate


def create_app(config_class: type = Config) -> Flask:
    import os

    app = Flask(__name__, instance_relative_config=False)
    root = os.path.dirname(os.path.abspath(__file__))
    app.static_folder = os.path.join(root, "static")
    app.template_folder = os.path.join(root, "templates")

    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    app.register_blueprint(school_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.get("/api/v1")
    def api_v1_redirect():
        """`/api/v1` (slash yok) → `/api/v1/` — blueprint yalnızca slashlı eşleşir."""
        return redirect(request.path + "/", code=308)

    app.wsgi_app = WhiteNoise(  # type: ignore[method-assign]
        app.wsgi_app,
        root=str(static_dir()),
        prefix="static/",
    )

    @app.cli.command("ensure-initial-data")
    def ensure_initial_data() -> None:
        """Veritabanında hiç bölüm yoksa demo seed çalıştırır."""
        from school.models import Department
        from school.seed import seed_demo_data

        n = db.session.scalar(select(func.count()).select_from(Department))
        if n and n > 0:
            click.echo("Seed skipped: database already has departments.")
            return
        click.echo("Running initial seed…")
        seed_demo_data()
        click.echo("Initial data ready.")

    @app.cli.command("seed-demo")
    def seed_demo_cmd() -> None:
        from school.seed import seed_demo_data

        seed_demo_data()

    return app

"""initial task_item table

Revision ID: ch09_0001
Revises:
Create Date: 2026-04-02

"""

from alembic import op
import sqlalchemy as sa


revision = "ch09_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "task_item",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("task_item")

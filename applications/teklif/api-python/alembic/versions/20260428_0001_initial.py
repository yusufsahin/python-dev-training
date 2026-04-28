"""initial tables

Revision ID: 20260428_0001
Revises:
Create Date: 2026-04-28
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260428_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cariler",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("unvan", sa.String(length=255), nullable=False),
        sa.Column("vergi_no", sa.String(length=20), nullable=False),
        sa.Column("eposta", sa.String(length=255), nullable=False),
        sa.Column("telefon", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "urunler",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tur", sa.String(length=16), nullable=False),
        sa.Column("ad", sa.String(length=255), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("barkod", sa.String(length=100), nullable=False),
        sa.Column("birim", sa.String(length=50), nullable=False),
        sa.Column("kdv_orani", sa.Integer(), nullable=False),
        sa.Column("satis_fiyati", sa.Float(), nullable=False),
        sa.Column("alis_fiyati", sa.Float(), nullable=False),
        sa.Column("doviz_kodu", sa.String(length=8), nullable=False),
        sa.Column("kategori", sa.String(length=100), nullable=False),
        sa.Column("fiyat_listesi_adi", sa.String(length=100), nullable=False),
        sa.Column("aktif", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "teklifler",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("cari_id", sa.String(length=64), nullable=False),
        sa.Column("para_birimi", sa.String(length=8), nullable=False),
        sa.Column("durum", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["cari_id"], ["cariler.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "teklif_kalemleri",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("teklif_id", sa.String(length=64), nullable=False),
        sa.Column("urun_id", sa.String(length=64), nullable=False),
        sa.Column("miktar", sa.Float(), nullable=False),
        sa.Column("birim_fiyat", sa.Float(), nullable=False),
        sa.Column("kdv_orani", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["teklif_id"], ["teklifler.id"]),
        sa.ForeignKeyConstraint(["urun_id"], ["urunler.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("teklif_kalemleri")
    op.drop_table("teklifler")
    op.drop_table("urunler")
    op.drop_table("cariler")

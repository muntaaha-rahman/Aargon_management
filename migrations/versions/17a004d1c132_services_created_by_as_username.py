"""services created_by as username

Revision ID: 17a004d1c132
Revises: 11de86d42518
Create Date: 2025-09-27 21:57:56.193264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17a004d1c132'
down_revision = '11de86d42518'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the foreign key first
    op.drop_constraint(op.f('services_created_by_fkey'), 'services', type_='foreignkey')

    # Then alter the column type
    op.alter_column(
        'services',
        'created_by',
        existing_type=sa.INTEGER(),
        type_=sa.String(length=100),
        existing_nullable=False
    )


def downgrade():
    # Revert column type back to INTEGER
    op.alter_column(
        'services',
        'created_by',
        existing_type=sa.String(length=100),
        type_=sa.INTEGER(),
        existing_nullable=False
    )

    # Recreate the foreign key
    op.create_foreign_key(
        op.f('services_created_by_fkey'),
        'services',
        'users',
        ['created_by'],
        ['id']
    )

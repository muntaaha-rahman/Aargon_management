from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13dc43a8f685'
down_revision = '1eac3a3b405b'
branch_labels = None
depends_on = None


def upgrade():
    # Add column with default True (for existing rows), allow nullable for now
    op.add_column(
        'users',
        sa.Column('active', sa.Boolean(), server_default=sa.true(), nullable=True)
    )

    # Set NOT NULL after backfill
    op.alter_column('users', 'active', nullable=False)

    # Add new value to userrole enum
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'client';")


def downgrade():
    # Remove column
    op.drop_column('users', 'active')
    # (Downgrading enums is tricky in Postgres, usually left empty)

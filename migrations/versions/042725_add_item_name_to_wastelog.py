"""Add item_name column to waste_logs table"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_item_name_field'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('waste_logs', sa.Column('item_name', sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('waste_logs', 'item_name')

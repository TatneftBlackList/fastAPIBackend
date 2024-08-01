"""fix user logs

Revision ID: 0efa8eb55a77
Revises: c03a2dd6c008
Create Date: 2024-08-01 14:27:09.474811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0efa8eb55a77'
down_revision: Union[str, None] = 'c03a2dd6c008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_request_logs_user_id_fkey', 'user_request_logs', type_='foreignkey')
    op.create_foreign_key(None, 'user_request_logs', 'auth', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_request_logs', type_='foreignkey')
    op.create_foreign_key('user_request_logs_user_id_fkey', 'user_request_logs', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###

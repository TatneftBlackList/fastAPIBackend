"""Fix foreign key for user request logs12

Revision ID: 1a4d7109e452
Revises: 47dffe2587d0
Create Date: 2024-08-01 14:30:14.861882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a4d7109e452'
down_revision: Union[str, None] = '47dffe2587d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

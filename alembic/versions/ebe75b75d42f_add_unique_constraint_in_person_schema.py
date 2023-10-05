"""add unique constraint in person schema

Revision ID: ebe75b75d42f
Revises: 43ddc52023e3
Create Date: 2023-07-22 15:19:24.680393

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ebe75b75d42f'
down_revision = '43ddc52023e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(constraint_name='person_email_unique',table_name='person',columns=["email"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('person_email_unique',"person")
    # ### end Alembic commands ###

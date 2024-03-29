"""moving to many-to-many relationships

Revision ID: 18ebeb04ef58
Revises: 5f79406514b0
Create Date: 2023-09-24 22:10:16.263222

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '18ebeb04ef58'
down_revision = '5f79406514b0'
branch_labels = None
depends_on = None

"""moving to many-to-many relationships

Revision ID: bd1a4b6e4528
Revises: 5f79406514b0
Create Date: 2023-09-24 21:22:20.453779


"""


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_table('hero')
    op.drop_table('team')
    # op.drop_table('hero_team_link')



    op.create_table('team',
                    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('team_id_seq'::regclass)"),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
                    sa.Column('headquarters', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='team_pkey'),
                    postgresql_ignore_search_path=False
                    )

    op.create_table('hero',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('secret_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['team_id'], ['team.id'], name='hero_team_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='hero_pkey')
                    )

    op.create_table('hero_team_link',
                    sa.Column('team_id', sa.INTEGER(), default=None, ),
                    sa.Column('hero_id', sa.INTEGER(), default=None),
                    sa.ForeignKeyConstraint(["hero_id"], ["hero.id"], name='hero_team_link_hero_id_fkey'),
                    sa.ForeignKeyConstraint(["team_id"], ["team.id"], name='hero_team_link_team_id_fkey'),
                    sa.PrimaryKeyConstraint('team_id', 'hero_id', name='hero_team_link_pkey'))

    # op.create_table('users', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    #                 sa.Column('user_name', sa.VARCHAR(length=50), nullable=True),
    #                 sa.PrimaryKeyConstraint('id', name='users_pkey'))
    # op.create_table('roles', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    #                 sa.Column('role_name', sa.VARCHAR(length=50), nullable=True),
    #                 sa.PrimaryKeyConstraint('id', name='roles_pkey'))
    # op.create_table('user_roles', sa.Column('user_id', sa.INTEGER(), nullable=True),
    #                 sa.Column('role_id', sa.INTEGER(), nullable=True),
    #                 sa.ForeignKeyConstraint(['roles_id'], ['roles.id'], name='user_roles_roles_id_fkey'),
    #                 sa.ForeignKeyConstraint(['users_id'], ['users.id'], name='user_roles_users_id_fkey'), )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    # op.drop_table('employees')
    op.drop_table('hero')
    op.drop_table('team')
    op.drop_table('hero_team_link')
    # op.drop_table('user_roles')
    # op.drop_table('roles')
    # op.drop_table('users')
    # ### end Alembic commands ###

from flask_admin.contrib.peewee import ModelView


class CommandView(ModelView):
    """
    View da model Command, com a exclusão da coluna 'id' da tela de admin,
    pois não é interessante exibir este dado.
    """
    column_exclude_list = ('id',)

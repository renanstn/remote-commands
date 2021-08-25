from flask_admin.contrib.peewee import ModelView


class CommomView(ModelView):
    """
    View padrão das models, com a exclusão da coluna 'id' da tela de admin,
    pois não é interessante exibir este dado.
    """
    column_exclude_list = ('id',)

from admin.models.view import SecureModelView


class EcoActivityModelView(SecureModelView):
    column_labels = {
        'name': 'Название'
    }
    form_columns = ['name']
from admin.models.view import SecureModelView


class DistrictModelView(SecureModelView):
    form_columns = ['name']
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Название района'
    }


from admin.models.view import SecureModelView


class MunicipalModelView(SecureModelView):
    form_columns = ['district', 'name', 'invite_link']
    column_searchable_list = ['name', 'district.name']
    column_default_sort = [('district.name', False), ('name', False)]
    column_labels = {
        'district': 'Район',
        'name': 'Название',
        'invite_link': 'Ссылка на чат',
    }

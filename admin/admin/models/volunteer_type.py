from admin.models.view import SecureModelView


class VolunteerTypeModelView(SecureModelView):
    form_columns = ['name']
    column_labels = {
        'name': 'Название'
    }

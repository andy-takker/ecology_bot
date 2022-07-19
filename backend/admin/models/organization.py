from admin.models.view import SecureModelView


class OrganizationModelView(SecureModelView):
    column_list = ['name','is_checked','creator','districts','eco_activities']
    column_searchable_list = ['name']
    column_labels = {
        'creator': 'Создатель организации',
        'eco_activities': 'Активности',
        'districts': 'Районы',
        'events': 'События',
        'created_at': 'Создано',
        'updated_at': 'Обновлено',
        'name': 'Название',
        'is_checked': 'Проверена?',
        'is_superorganization': 'Суперорганизация?'
    }

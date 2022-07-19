from admin.models.view import SecureModelView


class EventModelView(SecureModelView):
    column_list = ['name', 'description', 'organization', 'type', ]
    column_labels = {
        'organization': 'Организация',
        'created_at': 'Создано',
        'updated_at': 'Обновлено',
        'name': 'Название',
        'description': 'Описание',
        'type': 'Тип',
        'districts': 'Районы',
        'municipals': 'Муниципальные образования',
        'eco_activities': 'Активности',
        'volunteer_types': 'Виды волонтеров',
    }
    form_columns = ['name', 'description', 'organization', 'districts',
                    'municipals', 'volunteer_types']

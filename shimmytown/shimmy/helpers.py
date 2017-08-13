from django.apps import apps

def get_model_choices():
    '''
    Used to select from available models for Database queries
    '''

    models_list = [('','------')]
    for app_name,models in apps.all_models.items():
        for key,this_model in models.items():
            models_list.append((
                '.'.join([app_name,this_model.__name__]),
                this_model.__name__ + ' (in ' + app_name + ')'))
    return models_list

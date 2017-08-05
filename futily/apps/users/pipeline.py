def get_email(backend, user, response, is_new=False, *args, **kwargs):
    if backend.name == 'github' and is_new and not response.get('email', None):
        return {'email': 'dangamble89@gmail.com'}

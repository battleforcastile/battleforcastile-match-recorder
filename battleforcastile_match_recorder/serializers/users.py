def serialize_user(user):
    return {
        'username': user.username,
        'email': user.email,
    }
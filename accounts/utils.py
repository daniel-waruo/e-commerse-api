def token_creator(token_model, user, serializer):
    if token_model.objects.filter(user=user).exists():
        token, _ = token_model.objects.create(user=user)
    else:
        token = token_model.objects.get(user=user)
    return token

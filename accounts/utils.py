def create_knox_token(token_model, user, serializer):
    instance, token = token_model.objects.create(user=user)
    return token

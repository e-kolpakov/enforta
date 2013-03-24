def public_view(func):
    func.is_public = True
    return func
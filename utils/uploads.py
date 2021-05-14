def avatar_upload(instance, filename):
    return f"auth_/avatars/{instance.user.username}.{'jpg'}"


def brand_logo_upload(instance, filename):
    return f"auth_/brand/logos/{instance.name}.{'jpg'}"


def product_upload(instance, filename):
    return f"core/products/images/{instance.product.name}.jpg"

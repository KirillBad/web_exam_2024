from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.role.name in roles:
                return func(*args, **kwargs)
            else:
                flash("У вас нет прав для доступа к этой странице", category="error")
                return redirect(url_for('views.home_page'))
        return wrapper
    return decorator

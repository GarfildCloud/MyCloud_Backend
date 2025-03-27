import logging
from functools import wraps

logger = logging.getLogger("core")


def log_action(action: str):
    def decorator(view_method):
        @wraps(view_method)
        def wrapper(self, request, *args, **kwargs):
            user = getattr(request, 'user', None)
            username = user.username if user and user.is_authenticated else 'Anonymous'

            try:
                response = view_method(self, request, *args, **kwargs)
                logger.info(f"[{username}] ✅ {action}")
                return response
            except Exception as e:
                logger.warning(f"[{username}] ❌ {action} — ошибка: {str(e)}")
                raise

        return wrapper

    return decorator

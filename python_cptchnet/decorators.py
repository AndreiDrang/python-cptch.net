from .errors import CaptchaError
from .config import JSON_RESPONSE


def api_key_check(func):
    """
    Декоратор проверяет переданный параметр `service_key` на корректность
    """

    def wrapper(self, *args, **kwargs):
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()
        # проверяет длинну ключа API
        if len(self.post_payload.get("key")) == 32:
            return func(self, *args, **kwargs)
        else:
            self.result.update(
                {
                    "error": True,
                    "errorBody": CaptchaError().errors("ERROR_WRONG_USER_KEY"),
                }
            )
            return self.result

    return wrapper

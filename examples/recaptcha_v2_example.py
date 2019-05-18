import asyncio

from python_cptchnet import ReCaptchaV2


# Введите ключ от cptch.net из своего аккаунта
SERVICE_KEY = ""
"""
Этот пример показывает работу модуля решения ReCaptcha v2 New
"""
# Google sitekey
SITE_KEY = "6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ"
# ссылка на страницу с капчёй
PAGE_URL = "http://85.255.8.26/"

# Пример работы с модулем ReCaptchaV2
answer_usual_re2 = ReCaptchaV2.ReCaptchaV2(service_key=SERVICE_KEY).captcha_handler(
    site_key=SITE_KEY, page_url=PAGE_URL
)
print(answer_usual_re2)
"""
answer_... - это JSON строка с соответствующими полями

captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
	{
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
"""
# обычная recaptcha v2
if not answer_usual_re2["error"]:
    # решение капчи
    print(answer_usual_re2["captchaSolve"])
    print(answer_usual_re2["taskId"])
elif answer_usual_re2["error"]:
    # Тело ошибки, если есть
    print(answer_usual_re2["errorBody"]["text"])
    print(answer_usual_re2["errorBody"]["id"])


"""
Пример асинхронной работы 
"""


async def run():
    try:
        answer_aio_re2 = await ReCaptchaV2.aioReCaptchaV2(
            service_key=SERVICE_KEY
        ).captcha_handler(site_key=SITE_KEY, page_url=PAGE_URL)
        if not answer_aio_re2["error"]:
            # решение капчи
            print(answer_aio_re2["captchaSolve"])
            print(answer_aio_re2["taskId"])
        elif answer_aio_re2["error"]:
            # Тело ошибки, если есть
            print(answer_aio_re2["errorBody"]["text"])
            print(answer_aio_re2["errorBody"]["id"])
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

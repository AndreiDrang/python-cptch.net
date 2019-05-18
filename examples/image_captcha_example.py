import requests
import asyncio
import base64

from python_cptchnet import ImageCaptcha



"""
Этот пример показывает то как нужно работать с модулем для распознования обычной капчи изображением,
на примере нашего сайта.
В общем случае вам потребуется получение:
1. Получить ссылку на изображение капчи(сртрока 15 в примере)
2. Передать эту ссылку в модуль ImageCaptcha(строка 20 в примере)
"""
# Введите ключ от cptch.net из своего аккаунта
SERVICE_KEY = "2597d7cb1f9435a3b531ac283ce987d5"
# Для получения ссылки на обычную капчу нужно послать GET запрос с соответствующим парметром
image_link = requests.get(
    "http://85.255.8.26/api/", params={"captcha_type": "get_common_captcha"}
).json()["captcha_src"]

"""
contextmanager пример
"""

# синхронный пример contextmanager
with ImageCaptcha.ImageCaptcha(
    service_key=SERVICE_KEY,
    img_path="test_files",
    img_clearing=True,
    save_format="const"
) as img_captcha:
    result = img_captcha.captcha_handler(captcha_link=image_link)
    print(result)


# асинхронный пример contextmanager
async def aiocontext():
    with ImageCaptcha.aioImageCaptcha(
        service_key=SERVICE_KEY,
        img_path="test_files",
        img_clearing=True,
        save_format="const",
    ) as img_captcha:
        result = await img_captcha.captcha_handler(captcha_link=image_link)
        print(result)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(aiocontext())
    loop.close()

"""
Синхронный метод


Тут нужно воспользоваться бибилотекой, отослать на решение ссылку на капчу и получить ответ
далее его записать в user_answer
Первый пример демонстрирует сохранеие файла изображения как обычного файла в папу
"""

user_answer_const = ImageCaptcha.ImageCaptcha(
    service_key=SERVICE_KEY,
    img_path="test_files",
    img_clearing=False,
    save_format="const",
).captcha_handler(captcha_link=image_link)
print(user_answer_const)
"""
Второй пример демонстрирует сохранения файла как временного (temporary) - это стандартный вариант сохранения. 
Было выяснено, что он не работает с некоторыми видами капч - если возникают проблемы, то стоит использовать первый 
вариант
"""
user_answer_temp = ImageCaptcha.ImageCaptcha(
    service_key=SERVICE_KEY, save_format="temp"
).captcha_handler(captcha_link=image_link)
print(user_answer_temp)

"""
Пример работы с декодированием в base64 файла-капчи "налету"
An example of working with decoding in base64 a captcha file after downloading. 
"""
base_64_link = base64.b64encode(
    requests.get(
        "http://85.255.8.26/static/image/common_image_example/862963.png"
    ).content
).decode("utf-8")

user_answer_base64 = ImageCaptcha.ImageCaptcha(
    service_key=SERVICE_KEY
).captcha_handler(captcha_base64=base_64_link)
print(user_answer_base64)
"""
user_answer_... - это JSON строка с соответствующими полями
captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
    {
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
"""

if not user_answer_const["error"]:
    # решение капчи
    print(user_answer_const["captchaSolve"])
    print(user_answer_const["taskId"])
elif user_answer_const["error"]:
    # Тело ошибки, если есть
    print(user_answer_const["errorBody"]["text"])
    print(user_answer_const["errorBody"]["id"])

if not user_answer_temp["error"]:
    # решение капчи
    print(user_answer_temp["captchaSolve"])
    print(user_answer_temp["taskId"])
elif user_answer_temp["error"]:
    # Тело ошибки, если есть
    print(user_answer_temp["errorBody"]["text"])
    print(user_answer_temp["errorBody"]["id"])

if not user_answer_base64["error"]:
    # решение капчи
    print(user_answer_base64["captchaSolve"])
    print(user_answer_base64["taskId"])
elif user_answer_base64["error"]:
    # Тело ошибки, если есть
    print(user_answer_base64["errorBody"]["text"])
    print(user_answer_base64["errorBody"]["id"])

"""
Пример для работы с локальными файлами
"""
# папка в которой находится изображение, один из вариантов написания
captcha_file = "088636.png"

# так же есть возможность передать так:
# captcha_file = r'D:\Python\933588.png'
# captcha_file = 'D:\/Python\/933588.png'
try:
    user_answer_local = ImageCaptcha.ImageCaptcha(
        service_key=SERVICE_KEY
    ).captcha_handler(captcha_file=captcha_file)
    if not user_answer_local["error"]:
        # решение капчи
        print(user_answer_local["captchaSolve"])
        print(user_answer_local["taskId"])
    elif user_answer_local["error"]:
        # Тело ошибки, если есть
        print(user_answer_local["errorBody"]["text"])
        print(user_answer_local["errorBody"]["id"])

# отлов ошибки при проблемах чтения файла-изображения
except Exception as err:
    print(err)
"""
Асинхронный пример
Асинхронный способ поддерживает все параметры обычного метода
UPDATE 1.6.2
Добавлена поддержка прокси для асинхронного метода
!!!Поддерживаются только HTTP прокси!!!
Подробнее про него можно посмотреть тут:
https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support
"""


async def run():
    try:
        answer_aio_image = await ImageCaptcha.aioImageCaptcha(
            service_key=SERVICE_KEY
        ).captcha_handler(captcha_link=image_link)
        print(answer_aio_image)
        if not answer_aio_image["error"]:
            # решение капчи
            print(answer_aio_image["captchaSolve"])
            print(answer_aio_image["taskId"])
        elif answer_aio_image["error"]:
            # Тело ошибки, если есть
            print(answer_aio_image["errorBody"]["text"])
            print(answer_aio_image["errorBody"]["id"])
    except Exception as err:
        print(err)

    """
    Пример для работы с локальными файлами
    """
    # папка в которой находится изображение, один из вариантов написания
    # captcha_file = r'D:\Python\933588.png'
    # так же есть возможность передать так:
    # captcha_file = 'D:\/Python\/933588.png'

    try:
        answer_aio_local_image = await ImageCaptcha.aioImageCaptcha(
            service_key=SERVICE_KEY
        ).captcha_handler(captcha_file=captcha_file)
        print(answer_aio_local_image)
        if not answer_aio_local_image["error"]:
            # решение капчи
            print(answer_aio_local_image["captchaSolve"])
            print(answer_aio_local_image["taskId"])
        elif answer_aio_local_image["error"]:
            # Тело ошибки, если есть
            print(answer_aio_local_image["errorBody"]["text"])
            print(answer_aio_local_image["errorBody"]["id"])
    except Exception as err:
        print(err)
    """
    UPDATE 1.6.2 с прокси
    !!!Поддерживаются только HTTP прокси!!!
    """
    try:
        answer_aio_image = await ImageCaptcha.aioImageCaptcha(
            service_key=SERVICE_KEY
        ).captcha_handler(captcha_link=image_link, proxy="http://85.21.83.186:8080")
        if not answer_aio_image["error"]:
            # решение капчи
            print(answer_aio_image["captchaSolve"])
            print(answer_aio_image["taskId"])
        elif answer_aio_image["error"]:
            # Тело ошибки, если есть
            print(answer_aio_image["errorBody"]["text"])
            print(answer_aio_image["errorBody"]["id"])
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()

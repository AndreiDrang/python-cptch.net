# Сервер для отправки данных
url_request = "http://cptch.net/in.php"
# Сервер для получения ответа
url_response = "http://cptch.net/res.php"
# ключ приложения
app_key = "108"

"""
JSON возвращаемы пользователю после решения капчи

captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
    {
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
"""
JSON_RESPONSE = {
    "captchaSolve": None,
    "taskId": None,
    "error": False,
    "errorBody": {"text": None, "id": 0},
}


# генератор в котором задаётся кол-во поптыок на повторное подключение
def connect_generator():
    for i in range(5):
        yield i

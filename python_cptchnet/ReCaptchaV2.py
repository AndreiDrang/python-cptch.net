import requests
import time
import asyncio
import aiohttp

from python_cptchnet.config import app_key
from python_cptchnet.errors import CaptchaError
from python_cptchnet.result_handler import get_sync_result, get_async_result
from python_cptchnet.decorators import api_key_check
from python_cptchnet.config import url_request, url_response


class ReCaptchaV2:
	"""
	Класс служит для работы с новой ReCaptcha от Гугла и Invisible ReCaptcha.
	Для работы потребуется передать ключ от Сервиса, затем ключ сайта(подробности его получения в описании на сайте)
	И так же ссылку на сайт.
	"""

	def __init__(
			self,
			service_key: str,
			sleep_time: int = 10
	):
		"""
		Инициализация нужных переменных.
		:param service_key:  АПИ ключ капчи из кабинета пользователя
		:param sleep_time: Вермя ожидания решения капчи
		"""
		# время ожидания решения капчи
		self.sleep_time = sleep_time

		# пайлоад POST запроса на отправку капчи на сервер
		self.post_payload = {
			"key": service_key,
			"method": "userrecaptcha",
			"json": 1,
			"soft_id": app_key,
		}

		# пайлоад GET запроса на получение результата решения капчи
		self.get_payload = {"key": service_key, "action": "get", "json": 1}

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if exc_type:
			return False
		return True

	@api_key_check
	def captcha_handler(self, site_key: str, page_url: str, **kwargs):
		"""
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча
		:param kwargs: Для передачи дополнительных параметров
		:return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }		
		"""
		# result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия

		# Если переданы ещё параметры - вносим их в get_payload
		if kwargs:
			for key in kwargs:
				self.get_payload.update({key: kwargs[key]})

		self.post_payload.update({"googlekey": site_key, "pageurl": page_url})
		# получаем ID капчи
		captcha_id = requests.post(url_request, data=self.post_payload).json()

		# если вернулся ответ с ошибкой то записываем её и возвращаем результат
		if captcha_id["status"] == 0:
			self.result.update(
				{
					"error": True,
					"errorBody": CaptchaError().errors(captcha_id["request"]),
				}
			)
			return self.result
		# иначе берём ключ отправленной на решение капчи и ждём решения
		else:
			captcha_id = captcha_id["request"]
			# вписываем в taskId ключ отправленной на решение капчи
			self.result.update({"taskId": captcha_id})
			# обновляем пайлоад, вносим в него ключ отправленной на решение капчи
			self.get_payload.update({"id": captcha_id})

			# если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
			if self.post_payload.get("pingback"):
				return self.get_payload

			else:
				# Ожидаем решения капчи 10 секунд
				time.sleep(self.sleep_time)
				return get_sync_result(
					get_payload=self.get_payload,
					sleep_time=self.sleep_time,
					url_response=url_response,
					result=self.result,
				)


# асинхронный метод для решения РеКапчи 2
class aioReCaptchaV2:
	"""
	Класс служит для асинхронной работы с новой ReCaptcha от Гугла и Invisible ReCaptcha.
	Для работы потребуется передать ключ от сервиса, затем ключ сайта(подробности его получения в описании на сайте)
	И так же ссылку на сайт.
	"""

	def __init__(
			self,
			service_key: str,
			sleep_time: int = 10
	):
		"""
		Инициализация нужных переменных.
		:param service_key:  АПИ ключ капчи из кабинета пользователя
		:param sleep_time: Время ожидания решения капчи
		"""
		# время ожидания решения капчи
		self.sleep_time = sleep_time
		# пайлоад POST запроса на отправку капчи на сервер
		self.post_payload = {
			"key": service_key,
			"method": "userrecaptcha",
			"json": 1,
			"soft_id": app_key,
		}

		# пайлоад GET запроса на получение результата решения капчи
		self.get_payload = {"key": service_key, "action": "get", "json": 1}

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if exc_type:
			return False
		return True

	# Работа с капчей
	async def captcha_handler(self, site_key: str, page_url: str, **kwargs):
		"""
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча
		:param kwargs: Для передачи дополнительных параметров
		:return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }
		"""
		# result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия

		# Если переданы ещё параметры - вносим их в get_payload
		if kwargs:
			for key in kwargs:
				self.get_payload.update({key: kwargs[key]})

		self.post_payload.update({"googlekey": site_key, "pageurl": page_url})
		# получаем ID капчи
		async with aiohttp.ClientSession() as session:
			async with session.post(url_request, data=self.post_payload) as resp:
				captcha_id = await resp.json()

		# если вернулся ответ с ошибкой то записываем её и возвращаем результат
		if captcha_id["status"] == 0:
			self.result.update(
				{
					"error": True,
					"errorBody": CaptchaError().errors(captcha_id["request"]),
				}
			)
			return self.result
		# иначе берём ключ отправленной на решение капчи и ждём решения
		else:
			captcha_id = captcha_id["request"]
			# вписываем в taskId ключ отправленной на решение капчи
			self.result.update({"taskId": captcha_id})
			# обновляем пайлоад, вносим в него ключ отправленной на решение капчи
			self.get_payload.update({"id": captcha_id})

			# если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
			if self.post_payload.get("pingback"):
				return self.get_payload

			else:
				# Ожидаем решения капчи
				await asyncio.sleep(self.sleep_time)
				return await get_async_result(
					get_payload=self.get_payload,
					sleep_time=self.sleep_time,
					url_response=url_response,
					result=self.result,
				)

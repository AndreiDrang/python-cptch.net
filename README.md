# python-cptchnet

Библиотека предназначена для разрабаотчиков ПО и служит для облегчения работы с API сервиса Cptch.net.

Присутствуют [примеры работы с библиотекой](https://github.com/AndreiDrang/python-cptch.net/tree/master/examples).

**Используется Python версии 3.6+.**

## How to install? Как установить?

### pip

```bash
pip install python-cptchnet
```


### Source
```bash
git https://github.com/AndreiDrang/python-cptch.net.git
cd python-cptch.net
python setup.py install
```
***
По всем вопросам можете писать в [Telegram](https://t.me/joinchat/CD2EtQ5Pm0dmoSQQMTkVlw) чат.
***
### Последние обновления
**v.0.1** - 
***
### Реализованы следующие методы:


1.[Решение капчи-изображения(большие и маленькие).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ImageCaptcha.py)

Краткий пример:
```python
from python_cptchnet import ImageCaptcha
# Введите ключ от сервиса Cptch.net, из своего аккаунта
SERVICE_KEY = ""
# Ссылка на изображения для расшифровки
image_link = ""
# Возвращается JSON содержащий информацию для решения капчи
user_answer = ImageCaptcha.ImageCaptcha(service_key=SERVICE_KEY).captcha_handler(captcha_link=image_link)

if not user_answer['error']:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['error']:
	# Тело ошибки, если есть
	print(user_answer['errorBody']['text'])
	print(user_answer['errorBody']['id'])
```

2.[Решение ReCaptcha v2.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV2.py)

Краткий пример:
```python
from python_cptchnet import ReCaptchaV2
# Введите ключ от сервиса Cptch.net, из своего аккаунта
SERVICE_KEY = ""
# G-ReCaptcha ключ сайта
SITE_KEY = ""
# Ссылка на страницу с капчёй
PAGE_URL = ""
# Возвращается JSON содержащий информацию для решения капчи
user_answer = ReCaptchaV2.ReCaptchaV2(service_key=SERVICE_KEY).captcha_handler(site_key=SITE_KEY,
                                                                               page_url=PAGE_URL)

if not user_answer['error']:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['error']:
	# Тело ошибки, если есть
	print(user_answer['errorBody']['text'])
	print(user_answer['errorBody']['id'])
```

Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](http://85.255.8.26/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.
***
### Errors table
| Error ID       | Ошибка
| ------------- |:-------------:|
| -1      | Внутренняя ошибка (в соединении и т.п.), не относится к сервису Cptch.net

| Error ID       | in.php Cptch.net код ошибки
| ------------- |:-------------:|
| 10      | ERROR_WRONG_USER_KEY 
| 11      | ERROR_KEY_DOES_NOT_EXIST 
| 12      | ERROR_ZERO_BALANCE      
| 13      | ERROR_PAGEURL 
| 14      | ERROR_NO_SLOT_AVAILABLE   
| 15      | ERROR_ZERO_CAPTCHA_FILESIZE         
| 16      | ERROR_TOO_BIG_CAPTCHA_FILESIZE 
| 17      | ERROR_WRONG_FILE_EXTENSION   
| 18      | ERROR_IMAGE_TYPE_NOT_SUPPORTED       
| 19      | ERROR_UPLOAD 
| 20      | ERROR_IP_NOT_ALLOWED  
| 21      | IP_BANNED        
| 22      | ERROR_BAD_TOKEN_OR_PAGEURL
| 23      | ERROR_GOOGLEKEY   
| 24      | ERROR_CAPTCHAIMAGE_BLOCKED     
| 25      | MAX_USER_TURN 

| Error ID      | res.php Cptch.net код ошибки
| ------------- |:-------------:| 
| 30      | CAPCHA_NOT_READY 
| 31      | ERROR_CAPTCHA_UNSOLVABLE  
| 32      | ERROR_WRONG_ID_FORMAT       
| 33      | ERROR_WRONG_CAPTCHA_ID 
| 34      | ERROR_BAD_DUPLICATES   
| 35      | REPORT_NOT_RECORDED   

| Error ID      | NNNN Cptch.net код ошибки
| ------------- |:-------------:|
| 40      | ERROR: 1001 
| 41      | ERROR: 1002  
| 42      | ERROR: 1003        
| 43      | ERROR: 1004 
| 44      | ERROR: 1005  

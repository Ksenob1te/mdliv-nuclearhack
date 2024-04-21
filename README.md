# Проект - metro-bot
* бот, у которого можно в свободной форме спросить про информацию о пассажиропотоке на станции метро.

# Модули системы

## Агрегирующий сервер

* Получает текстовые запросы от эндпоинтов
* Обращается к базе данных пассажиропотока
* Обращается к серверу языковой модели
* Возвращает текстовый ответ вебхуком на эндпоинт

### Запуск сервера
Распологается в директории `./api_server`
Для запуска этого сервера необходимо запустить модуль по этой же директории. Cервер запускается на http://localhost:8080/
Документацию по запущенной API можно найти на http://localhost:8080/docs

### Функциональность
Данный сервер выполняет связующее звено между telegram ботом и нейросетевым сервером

Так же сервер осуществляет полноценную генерацию повторных запросов к нейросети (получение результата осуществляется в 2 прохода):
1. Первый запрос к нейросетевому серверу осуществляет первичную обработку запроса пользователя и извлечение из него ключевых токенов, таких как ветка метро, дата указываемая в запросе, станция
2. Второй запрос осуществляет генерацию натурального текста, который будет возвращен пользователю, при этом при генерации будет использована дата из базы данных, полученными по ключам из первого пункта


## Сервер нейросети
! You need to specify network model before trying to startup the project. It should be in the project root dir, and (yeah, fun) it should be named `codellama-7b-instruct.Q4_K_S.gguf`

* Осуществляет взаимодействие с предобученной моделью нейросети (в нашем примере используется небольшая модель для демонстрации, ведь наши возможности серверных вычислений значительно ограничены)
### Запуск сервера
Распологается в директории `./mct_lim`
Для запуска этого сервера необходимо запустить модуль по этой же директории. Cервер запускается на http://localhost:8082/
Документацию по запущенной API можно найти на http://localhost:8082/docs

## Телеграмм бот

* Получает текстовый запрос от пользователя
* Держит вебхук для ответных сообщений от сервера
* Принимает обратый вебхук от сервера и отсылает результат пользователю

### Запуск сервера
Распологается в директории `./telegram_bot`
Для запуска этого сервера необходимо запустить модуль по этой же директории. Cервер запускается на http://localhost:8081/
Документацию по запущенной API можно найти на http://localhost:8081/docs


## Схема сервиса
![image](![Схема](https://github.com/Ksenob1te/mdliv-nuclearhack/assets/63819958/a5f3a76c-b7c9-4227-aa7d-0e2b79d477a2))

## LLM модель
Использовали **code Llama 7b instruct**  
![image](https://github.com/Ksenob1te/mdliv-nuclearhack/assets/54020145/cada1ee1-3753-4280-91ad-cbced0c6424c)

## Бот 
![image](https://github.com/Ksenob1te/mdliv-nuclearhack/assets/54020145/3f6d59d4-afed-4df9-bcf8-8b8d183253fc)

## Сервер
Powered by FastApi  
![image](https://github.com/Ksenob1te/mdliv-nuclearhack/assets/54020145/510405ec-ae8f-4cb7-bce7-92deb6604509)

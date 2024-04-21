# Проект - metro-bot
* бот, у которого можно в свободной форме спросить про информацию о пассажиропотоке на станции метро.

# Модули системы

## Агрегирующий сервер

* Получает текстовые запросы от эндпоинтов
* Обращается к базе данных пассажиропотока
* Обращается к серверу языковой модели
* Возвращает текстовый ответ вебхуком на эндпоинт

## Сервер нейросети

* Тут магический двойной проход llm

## Телеграмм бот

* Получает текстовый запрос от пользователя
* Держит вебхук для ответных сообщений от сервера

# Схема сервиса
![image](https://github.com/Ksenob1te/mdliv-nuclearhack/assets/54020145/8540d093-6628-46e1-a1b0-d8a5a7e9e86d)

# LLM модель
Использовали **code Llama 7b instruct**  
![image](https://github.com/Ksenob1te/mdliv-nuclearhack/assets/54020145/cada1ee1-3753-4280-91ad-cbced0c6424c)

# Бот 
![image](https://github.com/Ksenob1te/mdliv-nuclearhack/assets/54020145/3f6d59d4-afed-4df9-bcf8-8b8d183253fc)

# Сервер
Powered by FastApi  
![image](https://github.com/Ksenob1te/mdliv-nuclearhack/assets/54020145/510405ec-ae8f-4cb7-bce7-92deb6604509)


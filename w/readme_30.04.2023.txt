				Проект Яндекс.Лицей.(30.04.2023):
Введенние: проект предназначен для активных пользователей, желающих делится своими новостями.
Цель: создание проекта по теме "Блог" на основе требований к проекту и системы оценивания.
Описание технической работы:
	 Целью было реализовать:
1)обработку путей для пользовательского отображения в главном файле
2)шаблонную структуру файлов отображения (использовать шаблоны Flask)
3)стили Bootstrap в файлах отображения для приятного глазу интерфейса
4)API пользователей в отдельном файле с ресурсами
5)разделение на пользователей зарегистрированных и не зарегистрированных
6)проверку прав доступа к блогам
7)API блогов в отдельном файле с ресурсами
8)классы для хранения данных в базе данных
9)подключение к базе данных
10)тестирование API для пользователей
11)тестирование API для блогов
Выдвинутые требования:
1.Проект должен использовать базу данных для хранения данных о блогах и пользователях
2.Проект должен хэшировать пароли пользователей, а не хранить их в открытом виде
3.Проект не должен выдавать чужие личные блоги
4.Проект должен хранить информацию о текущем пользователе
5.Проект должен отдавать корректные коды ошибок при их обнаружении в запросах(400 - что-то не так с телом запроса;
401 - пользователь не авторизован;403 - у пользователя нет прав на совершение действия;404 - не найдено;409 - конфликт данных)
6.Проект должен реализовать обращения к базе данных через ORM
7.Проект должен реализовывать стили разметки Bootstrap
8.Проект должен реализовывать шаблоны Flask для наследования разметки (расширения)
9.Проект должен содержать тесты для проверки API пользователей
10.Проект должен содержать тесты для проверки API блогов
Использовавшиеся библиотеки:
-flask
-flask-wtf
-flask-login
-flask-restfull
-sqlalchemy
				Сборка проекта:
Командой pip install -r requirements.txt установить все необходимые компоненты.
				Запуск:
1)Находясь внутри виртуального окружения, командой python app.py запустить проект
2)Перейти в браузере по ссылке http://localhost:5000
3)Для работы с API служит ссылка http://localhost:5000/api
Запуск теста:
1)Находясь внутри виртуального окружения, командой python app.py запустить проект
2)Находясь внутри виртуального окружения, командой python app.py запустить проект(тесты должны вывести ОК)
				Возможности использования:
1.Просмотр публичных блогов.
2.Регистрация.
3.Вход.
4.Добавление новости.
5.Редактирование новости.
6.Удаление новости.
					API:
1)Пользователи:
1.Получить всех пользователей: GET http://localhost:5000/api/users
2.Получить одного пользователя: GET http://localhost:5000/api/users/<user_id>(user_id - УИН пользователя, которого хотим получить)
3.Создание юзера: POST http://localhost:5000/api/users
		Request body (ВСЕ ПОЛЯ ОБЯЗАТЕЛЬНЫ):

{
    "name": "username", // Имя пользователя в системе
    "about": "little description about user", // Биография пользователя
    "email": "test@gmail.com", // Почта пользователя
    "hashed_password": "123456", // Пароль пользователя в открытом виде
    "password_again": "123456" // Должен соответствовать полю hashed_password
}
4.Редактирование юзера: PUT http://localhost:5000/api/users/<user_id>
user_id - УИН пользователя, которого хотим редактировать
Request body (ВСЕ ПОЛЯ НЕ ОБЯЗАТЕЛЬНЫ):

{
    "name": "username 1", // Имя пользователя в системе
    "about": "little description about user 1", // Биография пользователя
    "email": "test1@gmail.com", // Почта пользователя
    "hashed_password": "1234561", // Пароль пользователя в открытом виде
    "password_again": "1234561" // Должен соответствовать полю hashed_password
}
При смене пароля, нужно обязательно указать поле password_again
5.Удалить юзера: DELETE http://localhost:5000/api/users/<user_id>(user_id - УИН пользователя, которого хотим удалить)
2)Блоги:
1.Получить все блоги: GET http://localhost:5000/api/news?is_authenticated=true&user_id=1
(Если is_authenticated и user_id не переданы (или неверные), тогда будут выданы только публичные записи)
2.Получить один блог: GET http://localhost:5000/api/news/<news_id>
(news_id - УИН блога, который хотим получить)
3.Создать блог: POST http://localhost:5000/api/news
Request body (ВСЕ ПОЛЯ ОБЯЗАТЕЛЬНЫ):

{
    "title": "Title of blog", // Заголовок блога
    "content": "Blog content. Whatever text you prefer", // Основной текст блога
    "user_id": 1, // УИН пользователя, от лица которого создаётся блог
    "is_private": false/true // Если false, запись будет доступна всем пользователям. Если true, только создателю
}
4.Редактировать блог:PUT http://localhost:5000/api/news/<news_id>
news_id - УИН блога, который хотим редактировать
Request body (ОБЯЗАТЕЛЬНО ТОЛЬКО ПОЛЕ user_id):

{
    "title": "Title of blog 1", // Заголовок блога
    "content": "Blog content. Whatever text you prefer 1", // Основной текст блога
    "user_id": 1, // УИН пользователя, от лица которого редактируется блог
    "is_private": false/true // Если false, запись будет доступна всем пользователям. Если true, только создателю
}
5.Удалить блог:DELETE http://localhost:5000/api/news/<news_id>?is_authenticated=true&user_id=1
news_id - УИН блога, который хотим удалить
user_id - УИН пользователя, от лица которого был создан блог
is_authenticated - вошёл ли пользователь в систему


		Работу выполняли: Алексей Овчинников и Переверзев Евгений.
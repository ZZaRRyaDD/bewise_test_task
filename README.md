Bewise

### Требования

Необходимо, чтобы были установлены следующие компоненты:

- `Docker`, `docker-compose`, `make`

### Запуск

1. Создание файла с переменными окружения
```commandline
make env
```

2. Запуск приложения:
```commandline
make docker-up-build
```

После запуска контейнеров по адресу ```0.0.0.0:8000/swagger``` будет доступна документация по API.

### Дополнительные команды

- Открытие базы данных внутри Docker-контейнера:
```commandline
make open-db
```

- Вывести список всех команд и их описание:
```commandline
make help
```

### Структура проекта

```app/config``` - находятся настройки проекта, в которых находятся параметры для подключения к базе данных

```app/db``` - отвечает за работу с базой данных

```app/endpoints``` - находятся энд-поинты для взаимодействия с сервером

```app/schemas``` - находятся схемы данных для получения запроса и отдачи ответа

```app/utils``` - находятся бизнес логика


### Описание работы алгоритма

1. На энд-поинт приходит запрос, в теле которого содержится количество получаемых вопросов.

2. В базу данных выполняется запрос на взятие последнего сохраненного вопроса.

3. Далее делается запрос на указанный в задании сервис с переданным значением количества.

4. Полученные объекты приводятся к pydantic-моделям.

5. Собираются id полученных вопросов и делается запрос в базу данных для получения уже существующих с данными id вопросов в базе данных.

6. Id полученных вопросов сохраняются в коллекции set, т.к. среди них могут быть повторяющиеся вопросы. Id существующих вопросов хранятся в коллекции set, т.к. она имеет асимптотическую сложность O(1) при проверке вхождения элемента в коллекцию.

7. Проходимся по всем полученным вопросам. Если вопроса еще нет в обработанных, то добавляем его в список на добавление в базу данных и добавляем его id в множество для обработанных. Если вопрос есть в обработанных, то мы проходимся циклом while с условием - пока данный элемент существует в базе данных и пока этот элемент существует в уже обработанных вопросах. В цикле мы делаем запрос на API, проверяем существование данного вопроса в базе данных. Если вопроса в базе данных нет и его нет в уже обработанных - добавляем данный вопрос в обработанные и добавляем на вставку в базу данных.

8. После прохождения по всем полученным по API объектам - добавляем объекты в базу данных и возвращаем полученный ранее последний сохраненный элемент до данного запроса.

### Примеры запросов

Запрос №1

```
Request:
Адрес: http://0.0.0.0:8000/questions
Метод: POST
Тело:
{
    "questions_num": 5
}

Response:
Статус ответа: 201
Тело ответа:
{
  "last_question": null
}
```

Запрос №2

```
Request:
Адрес: http://0.0.0.0:8000/questions
Метод: POST
Тело:
{
    "questions_num": 5
}

Response:
Статус ответа: 201
Тело ответа:
{
  "last_question": {
    "question_id": 50248,
    "question": "It sounds somewhat sexist, but a dominant partner is said to \"wear\" these \"in the family\"",
    "answer": "the pants",
    "created_at": "2022-12-30"
  }
}
```

Запрос №3

```
Request:
Адрес: http://0.0.0.0:8000/questions
Метод: POST
Тело:
{
    "questions_num": 0
}

Response:
Статус ответа: 400
Тело ответа:
{
  "detail": "Count question must be more one"
}
```

## Перед тем как начать работать

Перед тем как пытаться запустить все это дело, нужно скачать docker compose. Самый простой способ это сделать - ввести в консоль `docker pull docker/compose`

Рекомендую отдельно скачать необходимые образы:
  `docker pull redis`
  `docker pull mongo`
  `docker pull postgres`
  `docker pull neo4j`
  `docker pull elasticsearch:8.4.3`

## Как запускать:
1. Перейти в корневую папку проекта через консоль
2. Ввести `docker-compose up --build -d`  
Флаг --build пересобирает изменившиеся проекты с Dockerfile

## Как добавить свой сервис:
1. Создать Dockerfile в папке с сервисом
2. В `docker-compose.yaml` в разделе `services` вписать имя сервиса и указать через параметр `build` путь к Dockerfile'у. (Как пример смотреть `postgres-ma`)

# Рабочие сервисы:
## redis-ma:
Функционал: предоставляет информацию о студентах по id  
Api доступно по адресу `redis-ma:22808/api/students`.  
Список параметров: `/api/students/students=<id1>... ,<id2>`  
Пример: `http://redis-ma:22808/api/students?students=19ПЫ8781,19ЧТ8208`, `http://redis-ma:22808/api/students?students=19ПЫ8781`

## postgres-ma:
1. `postgres-ma:22808/api/students`  
Функционал: предоставляет информацию о всех студентах
Параметры не нужны  
Пример: `http://postgres-ma:22808/api/students`

2. `postgres-ma:22808/api/groups`  
Функционал: предоставляет информацию о всех студентах  
Параметры не нужны  
Пример: `http://postgres-ma:22808/api/groups`  

3. `postgres-ma:22808/api/students?lessons=<id>... ,<id>from=<date>&until=<date>`  
Функционал: Выдает 10 худших студентов по посещаемости предметов за период  
Параметры: id - int, date - "%d-%m-%Y"  
Возвращаемый формат: [{"id" : int, "visit_percent": float} ... ]  
Пример: `http://postgres-ma:22808/api/students?lessons=2,3,4&from=02-04-2019&until=04-09-2019`  

4. `postgres-ma:22808/api/lessons`  
Функционал: предоставляет информацию о всех предметах  
Параметры не нужны  
Пример: `http://postgres-ma:22808/api/lessons`  

5. `postgres-ma:22808/api/courses`  
Функционал: предоставляет информацию на каких курсах учится группа
Параметры не нужны  
Возвращаемый формат: [{"group_fk" : string, "course": int} ... ]  
Пример: `http://postgres-ma:22808/api/courses`  

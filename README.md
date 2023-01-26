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
Функционал: предоставляет информацию о всех студентах и группах
Api доступно по адресу `postgres-ma:22808/api/students`.  
Api доступно по адресу `postgres-ma:22808/api/groups`.  
Параметры не нужны  
Пример: `http://postgres-ma:22808/api/students`  
Пример: `http://postgres-ma:22808/api/groups`  

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
2. Ввести `docker-compose up -d`

## Как добавить свой сервис:
1. Создать Dockerfile в папке с сервисом
2. В `docker-compose.yaml` в разделе `services` вписать имя сервиса и указать через параметр `build` путь к Dockerfile'у. (Как пример смотреть `postgres-ma`)

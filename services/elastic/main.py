import os
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from flask import Flask, request
import logging
import time
from urllib.parse import urlparse, parse_qs, unquote
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

rows = [
    {
        "name": "Математика",
        "equipment": "учебники",
        "materials": "Область знаний, включающая изучение таких тем, как числа (арифметика и теория чисел), формулы и связанные с ними структуры (алгебра), формы и пространства, в которых они содержатся (геометрия), величины и их изменения (исчисление и анализ)",
    },
    {
        "name": "Русский язык",
        "equipment": "учебник",
        "materials": "Язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.",
    },
    {
        "name": "Английский язык",
        "equipment": "учебник",
        "materials": "Язык англо-фризской подгруппы западной группы германской ветви индоевропейской языковой семьи. ",
    },
    {
        "name": "История",
        "equipment": "учебник",
        "materials": "Наука, исследующая прошлое, реальные факты и закономерности смены исторических событий, эволюцию общества и отношений внутри него.",
    },
    {
        "name": "Информатика",
        "equipment": "компьютер",
        "materials": "Наука о методах и процессах сбора, хранения, обработки, передачи, анализа и оценки информации с применением компьютерных технологий, обеспечивающих возможность её использования для принятия решений. ",
    },{
        "name": "Сети",
        "equipment": "провода",
        "materials": "Система, обеспечивающая обмен данными между вычислительными устройствами - компьютерами, серверами, маршрутизаторами.",
    },
    {
        "name": "Труд",
        "equipment": "табуретка",
        "materials": "Деятельность человека, направленная на создание материальных и духовных благ, которые удовлетворяют потребности индивида и общества.",
    },
    {
        "name": "Физкультура",
        "equipment": "Носки",
        "materials": "Область социальной деятельности, направленная на сохранение и укрепление здоровья человека в процессе осознанной двигательной активности. ",
    },
    {
        "name": "Научная деятельность",
        "equipment": "Микроскоп",
        "materials": "Cовокупность целесообразных, предметно-направленных действий исследователя или группы исследователей по выработке, получению и теоретической систематизации объективных знаний о действительности.",
    },

]

app.logger.info("Start connecting")
time.sleep(15)
elastic = Elasticsearch("http://elastic:9200")
app.logger.info("Connected to elastic")

@app.route("/api/lessons", methods=["GET"])
def get_lessons():
    keyword = request.args.get('find', type = str)

    final_data = []
    
    if not keyword:
        app.logger.info(f"keyword = {keyword}")
        body = {'query':{"match_all": {}}}
        res= elastic.search(index='lesson_descriptions', filter_path=['hits.hits._source'], body=json.dumps(body))
        all_hits = res['hits']['hits']
        for num, doc in enumerate(all_hits):
            for value in doc.values():
                final_data.append(value)
        app.logger.info(final_data)
        return final_data

    body = {
        "query": {
        "multi_match" : {
            "query":  unquote(keyword),
            "fields": [ "equipment", "materials", "name" ]
        }
    }}
    app.logger.info(json.dumps(body, ensure_ascii=False))
    
    res = elastic.search(index="lesson_descriptions", filter_path=['hits.hits._source'], body=json.dumps(body, ensure_ascii=False))

    final_data = []
    all_hits = res['hits']['hits']

    app.logger.info(all_hits)

    for num, doc in enumerate(all_hits):
        for value in doc.values():
            final_data.append(value)

    app.logger.info(final_data)

    return final_data


    # res = elastic.search(index="lesson_descriptions", body={"query": {"match": {"content": "fox"}}})
    # print("%d documents found" % res['hits']['total'])
    # for doc in res['hits']['hits']:
    #     print("%s) %s" % (doc['_id'], doc['_source']['content']))
mappings = {
        "properties": {
            "name": {"type": "text", "analyzer": "standard"},
            "equipment": {"type": "text", "analyzer": "standard"},
            "materials": {"type": "text", "analyzer": "standard"},
    }
}

#elastic.delete_by_query(index="lesson_descriptions", body={"query": {"match_all": {}}})
elastic.indices.create(index="lesson_descriptions", mappings=mappings)
for i, row in enumerate(rows):
    doc = {
        "name": row["name"],
        "equipment": row["equipment"],
        "materials": row["materials"],
    }
    elastic.index(index="lesson_descriptions", id=i, document=doc)

app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])
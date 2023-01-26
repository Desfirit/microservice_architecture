import os
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from flask import Flask, request
import logging
from urllib.parse import urlparse, parse_qs, unquote
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

rows = [
    {
        "equipment": "учебники",
        "materials": "Математика. Область знаний, включающая изучение таких тем, как числа (арифметика и теория чисел), формулы и связанные с ними структуры (алгебра), формы и пространства, в которых они содержатся (геометрия), величины и их изменения (исчисление и анализ)",
    },
    {
        "equipment": "учебник",
        "materials": "Русский язык. Язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.",
    },
    {
        "equipment": "учебник",
        "materials": "Английский язык. Язык англо-фризской подгруппы западной группы германской ветви индоевропейской языковой семьи. ",
    },
    {
        "equipment": "учебник",
        "materials": "История. Наука, исследующая прошлое, реальные факты и закономерности смены исторических событий, эволюцию общества и отношений внутри него.",
    },
    {
        "equipment": "компьютер",
        "materials": "Информатика.Наука о методах и процессах сбора, хранения, обработки, передачи, анализа и оценки информации с применением компьютерных технологий, обеспечивающих возможность её использования для принятия решений. ",
    },{
        "equipment": "провода",
        "materials": "Сети. Система, обеспечивающая обмен данными между вычислительными устройствами - компьютерами, серверами, маршрутизаторами.",
    },
    {
        "equipment": "табуретка",
        "materials": "Труд. Деятельность человека, направленная на создание материальных и духовных благ, которые удовлетворяют потребности индивида и общества.",
    },
    {
        "equipment": "Носки",
        "materials": "Физкультура. Область социальной деятельности, направленная на сохранение и укрепление здоровья человека в процессе осознанной двигательной активности. ",
    },
    {
        "equipment": "Микроскоп",
        "materials": "Научная деятельность. совокупность целесообразных, предметно-направленных действий исследователя или группы исследователей по выработке, получению и теоретической систематизации объективных знаний о действительности.",
    },

]

def try_connect():
    try:
        return Elasticsearch("http://elastic:9200")
    except Exception:
        return None

elastic = try_connect()
@app.route("/api/lessons", methods=["GET"])
def get_lessons():
    keyword = request.args.get('find', type = str)
    final_data = []
    if not keyword:
        body = {'query':{"match_all": {}}}
        res= elastic.search(index='lesson_descriptions',body=json.dumps(body))
        all_hits = res['hits']['hits']
        for num, doc in enumerate(all_hits):
            for value in doc.values():
                final_data.append(value)
        app.logger.info(final_data)
    else:
        body = {
          "query": {
            "multi_match" : {
              "query":  keyword,
              "fields": [ "equipment", "materials" ]
            }
          }}
        app.logger.info(json.dumps(body, ensure_ascii=False))
        res = elastic.search(index="lesson_descriptions", body=json.dumps(body, ensure_ascii=False))
        # body = {'query': {'match': {'materials': 'ex'}}}
        # res2 = elastic.search(index="lesson_descriptions", body=json.dumps(body))
        final_data = []
        all_hits = res['hits']['hits']
        for num, doc in enumerate(all_hits):
            for value in doc.values():
                final_data.append(value)
        # all_hits = res2['hits']['hits']
        # for num, doc in enumerate(all_hits):
        #     for value in doc.values():
        #         final_data.append(value)
        app.logger.info(final_data)

    return final_data


    # res = elastic.search(index="lesson_descriptions", body={"query": {"match": {"content": "fox"}}})
    # print("%d documents found" % res['hits']['total'])
    # for doc in res['hits']['hits']:
    #     print("%s) %s" % (doc['_id'], doc['_source']['content']))
# mappings = {
#         "properties": {
#             "equipment": {"type": "text", "analyzer": "standard"},
#             "materials": {"type": "text", "analyzer": "standard"},
#     }
# }
#
# elastic.indices.create(index="lesson_descriptions", mappings=mappings)
# for i, row in enumerate(rows):
#     doc = {
#         "equipment": row["equipment"],
#         "materials": row["materials"],
#     }
#     elastic.index(index="lesson_descriptions", id=i, document=doc)

app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])
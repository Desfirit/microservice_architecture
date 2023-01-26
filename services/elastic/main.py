from elasticsearch import Elasticsearch

es = Elasticsearch(['http://elastic:9200'])

doc = {
    'material': 'шкура кота',
    'equipment': 'лопата',
}

resp = es.index(index="test-index", id=1, document=doc)
print(resp['result'])

# resp = es.get(index="test-index", id=1)
# print(resp['_source'])
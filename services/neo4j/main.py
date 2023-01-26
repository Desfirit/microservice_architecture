from flask import Flask, request, jsonify, redirect, render_template
from neo4j import GraphDatabase, Graph
import urllib.request
import csv
import logging
import sys
import time
import os
import json

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logging.getLogger("neo4j").addHandler(handler)
logging.getLogger("neo4j").setLevel(logging.DEBUG)

time.sleep(10)

# uri = "neo4j:22808"
# driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))
# session = driver.session()
# session.run("CREATE OR REPLACE DATABASE graphDb")
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.graph = Graph(uri, auth=(user, password))

    # Метод, который передает запрос в БД
    def query(self, query, db=None):
        assert self.graph is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            response = self.graph.run("CREATE (a:Person {name:{N}})", {"N": "Alice"})
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


students = []
req = urllib.request.Request(f"http://postgres-ma:{os.environ['LOCAL_SERVICES_PORT']}/api/students")
with urllib.request.urlopen(req) as response:
    the_page = response.read()
    students_list = json.loads(the_page)
    for obj in students_list:
        students.append(
            {
                "student_id": obj['id'],
                "group_id": obj['group_fk'],
            }
        )

req = urllib.request.Request(f"http://postgres-ma:{os.environ['LOCAL_SERVICES_PORT']}/api/groups")
with urllib.request.urlopen(req) as response:
    the_page = response.read()
    group_list = json.loads(the_page)
    for obj in group_list:
        for student in students:
            if student["group_id"] == obj['id']:
                student["speciality_id"] = obj['speciality_fk']

# print(students)
greeter = Neo4jConnection("http://neo4j:7687/", user=os.environ["NEO4J_USER"], password=os.environ["NEO4J_PASS"])

print("Succesfully connected to neo4j")


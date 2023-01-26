from flask import Flask, request, jsonify, redirect, render_template
from neo4j import GraphDatabase
import urllib.request
import csv
import logging
import sys
import time
import os

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
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()

    # Метод, который передает запрос в БД
    def query(self, query, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

req = urllib.request.Request(f"http://postgres-ma:{os.environ['LOCAL_SERVICES_PORT']}/api/students")
with urllib.request.urlopen(req) as response:
   the_page = response.read()
   print(the_page)

conn = Neo4jConnection(uri="neo4j:7687", user=os.environ["NEO4J_USER"], password=os.environ["NEO4J_PASS"])

print("Succesfully connected to neo4j")

conn.query("CREATE OR REPLACE DATABASE graphDb")
conn.query("SHOW DATABASE")

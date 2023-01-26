from flask import Flask, request, jsonify, redirect, render_template
from neo4j import GraphDatabase
import csv
import logging
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logging.getLogger("neo4j").addHandler(handler)
logging.getLogger("neo4j").setLevel(logging.DEBUG)
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


conn = Neo4jConnection(uri="neo4j:7687", user="neo4j", password="qwerty123")
conn.query("CREATE OR REPLACE DATABASE graphDb")
conn.query("SHOW DATABASE")

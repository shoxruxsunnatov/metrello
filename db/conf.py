import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect():
    return psycopg2.connect(
        dbname=os.environ.get("dbname"),
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        host=os.environ.get("host"),
        port=os.environ.get("port")
    )


connection = connect()

import json
import MySQLdb

class DbConnector:
    def __init__(self, config_file):
        self.config_file = config_file
        self.db = None
        self.cursor = None

    def load_config(self):
        try:
            with open(self.config_file) as file:
                config = json.load(file)
            return config
        except FileNotFoundError as e:
            print(f"Error: Configuration file not found. {e}")
        except json.JSONDecodeError as e:
            print(f"Error: JSON decode error. {e}")

    def connect(self):
        try:
            config = self.load_config()
            if config:
                self.db = MySQLdb.connect(
                    host=config['host'],
                    user=config['user'],
                    passwd=config['passwd']
                )
                self.cursor = self.db.cursor()
        except MySQLdb.Error as err:
            print(f"Error: Unable to connect to the database. {err}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.db.commit()
            return self.cursor.fetchone()
        except MySQLdb.Error as err:
            print(f"Error: Unable to execute query. {err}")
            return None

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
        except MySQLdb.Error as err:
            print(f"Error: Unable to close the connection. {err}")

# Usage
if __name__ == "__main__":
    db = DbConnector('config_file.json')
    db.connect()

    queries = [
        "SELECT VERSION()",
        "CREATE DATABASE IF NOT EXISTS dbs;",
        "USE dbs;",
        "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100), password VARCHAR(100), role VARCHAR(100));",
        "CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, bname VARCHAR(100), authname VARCHAR(100), price VARCHAR(100));"
    ]

    for query in queries:
        db.execute_query(query)

    db.close()

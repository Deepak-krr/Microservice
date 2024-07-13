import json
import MySQLdb

# Load database credentials from a JSON file
with open('config_file.json') as config_file:
    config = json.load(config_file)

# Connect to the database
db = MySQLdb.connect(
    host=config['host'],
    user=config['user'],
    passwd=config['passwd']
)

# Use a cursor to interact with the database
cursor = db.cursor()

# Example query to test the connection
try:
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print("Database version: {}".format(version[0]))
except MySQLdb.Error as err:
    print("Error: unable to fetch data. Error message: ", err)

# Close the cursor and connection
cursor.close()
db.close()

import os
import sqlite3
from datetime import datetime
from collections import defaultdict
from pprint import pprint
import base64


cur_dir = os.path.dirname(__file__)
# Define the SQLite database path
DATABASE =  os.path.join(cur_dir, 'pulpit.sqlite')

image_path = 'static/react/media/news1.5a3156d6965b41706085.jpg'

# Read the binary content of the image
with open(image_path, 'rb') as image_file:
    image_data = image_file.read()

# Connect to the SQLite db
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Update the image data in the database
cursor.execute('UPDATE News SET cover = ? where id = 5', (sqlite3.Binary(image_data),))

# Commit the changes and close the database connection
conn.commit()
conn.close()
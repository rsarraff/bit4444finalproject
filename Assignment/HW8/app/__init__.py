# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Import core packages
import os

# Import Flask 
from flask import Flask
import pymysql

# Inject Flask magic
app = Flask(__name__)
app.secret_key = "1234567890"

dbConn = pymysql.connect(
    host = "host.docker.internal",
    port = 3309,
    user = 'root',
    password = 'change-me',
    database ='northwind',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = dbConn.cursor()


# Import routing to render the pages
from app import views
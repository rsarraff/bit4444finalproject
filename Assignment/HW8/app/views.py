# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask  import render_template, request, redirect, url_for, flash
from jinja2 import TemplateNotFound

# App modules
from app import app, dbConn, cursor
# from app.models import Profiles

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/form')
def userForm():
    return render_template('userform.html')

@app.route('/hw8')
def HW8():
    # retrieve a list of supplier IDs from the Northwind database
    sql = "select SupplierID from Suppliers"
    cursor.execute(sql)
    suppids = cursor.fetchall()
    return render_template('hw8.html', suppids=suppids)

@app.route('/searchProducts', methods=['GET'])
def SearchProducts():
    # search for the product records for a given supplier ID
    sid = request.args.get('suppid')

    #search for the product records
    sql = "select * from Products where SupplierID=%s"
    print(cursor.mogrify(sql, sid))
    print(sid)
    cursor.execute(sql, sid)
    products = cursor.fetchall()

    return render_template('ProductTable.html', products=products)
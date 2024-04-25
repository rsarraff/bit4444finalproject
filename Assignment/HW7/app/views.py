# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask import render_template, request, redirect, url_for, flash
from jinja2 import TemplateNotFound

# App modules
from app import app , dbConn , cursor
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
    return render_template('hw7q2.html')


@app.route('/success')
def success():
    return render_template('success.html')
    

@app.route('/addproduct', methods=['POST'])
def addProduct():

    # Retrieve form data
    pid = request.form.get("pid")  # Can be None or empty for a new record
    pname = request.form.get("pname")
    sid = request.form.get("sid")
    cid = request.form.get("cid")
    unitsInStock = request.form.get("unitsInStock")
    unitPrice = request.form.get("unitPrice")

    # Validate inputs
    error = False
    if not pname:
        flash("Product name is required.")
        error = True
    if not sid or not sid.isdigit() or int(sid) <= 0:
        flash("Supplier ID must be a positive integer.")
        error = True
    if not cid or not cid.isdigit() or not 1 <= int(cid) <= 8:
        flash("Category ID must be an integer between 1 and 8.")
        error = True
    if not unitsInStock or not unitsInStock.isdigit() or int(unitsInStock) < 0:
        flash("Units in Stock must be a non-negative integer.")
        error = True
    if not unitPrice or not unitPrice.replace('.', '', 1).isdigit() or float(unitPrice) < 0:
        flash("Unit Price must be a non-negative number.")
        error = True

    if error:
        return render_template('hw7q2.html', pid=pid, pname=pname, sid=sid, cid=cid, unitsInStock=unitsInStock, unitPrice=unitPrice)

    if pid:  # Update operation
        sql = "UPDATE Products SET ProductName = %s, SupplierID = %s, CategoryID = %s, UnitsInStock = %s, UnitPrice = %s WHERE ProductID = %s"
        cursor.execute(sql, (pname, sid, cid, unitsInStock, unitPrice, pid))
        flash("Product updated successfully.")
    else:  # Insert operation
        sql = "INSERT INTO Products (ProductName, SupplierID, CategoryID, UnitsInStock, UnitPrice) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (pname, sid, cid, unitsInStock, unitPrice))
        flash("Product added successfully.")
    
    dbConn.commit()
    return redirect(url_for('success'))

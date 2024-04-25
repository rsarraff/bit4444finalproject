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

@app.route('/updateSupplier', methods=['GET', 'POST'])
def updateSupplier():
    if request.method == 'POST':
        supplier_id = request.form.get("SupplierID")
        company_name = request.form.get("CompanyName")
        city = request.form.get("City")
        country = request.form.get("Country")

        error = False
        if not supplier_id or not supplier_id.isdigit() or int(supplier_id) <= 0:
            flash("Supplier ID must be a positive integer.")
            error = True
        if not company_name:
            flash("Company Name is required.")
            error = True
        if not city:
            flash("City is required.")
            error = True
        if not country:
            flash("Country is required.")
            error = True

        if error:
            return render_template('updateSupplier.html', SupplierID=supplier_id, CompanyName=company_name, City=city, Country=country)

        sql = "UPDATE Suppliers SET CompanyName = %s, City = %s, Country = %s WHERE SupplierID = %s"
        cursor.execute(sql, (company_name, city, country, supplier_id))
        dbConn.commit()
        flash("Supplier updated successfully.")
        return redirect(url_for('success'))

    return render_template('updateSupplier.html', 
                           SupplierID=request.form.get('SupplierID', ''),
                           CompanyName=request.form.get('CompanyName', ''),
                           City=request.form.get('City', ''),
                           Country=request.form.get('Country', ''))
@app.route('/success')
def success():
    return render_template('success.html')

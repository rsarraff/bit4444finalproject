# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, json
from jinja2  import TemplateNotFound

# App modules
from app import app, dbConn, cursor
# from app.models import Profiles

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/addProduct')
def userForm():
    return render_template('aProduct.html')

@app.route('/addProductForm', methods=['POST'])
def addProduct():
    pid = request.form.get("pid")
    pname = request.form.get("pname")
    pdescription = request.form.get("pdescription")
    unitp = request.form.get("unitprice")
    pcategory = request.form.get("pcategory")
    pquantity = request.form.get("pquantity")
    image = request.form.get("urlimage")
    verify = request.form.get("verify")

    error = False
    if not verify:
        flash("Box must be checked to verify.")
        error = True

    if not pid or not pid.isdigit():
        flash("Product ID must be a number.")
        error = True
    else:
        cursor.execute("SELECT 1 FROM ProductProfile WHERE PID = %s", (pid,))
        if cursor.fetchone() is not None:
            flash("There is already a product with the same ID.")
            error = True
        
    if not pname:
        flash("Product name is required.")
        error = True
    if not pdescription:
        flash("Product description is required.")
        error = True
    if not unitp or not unitp.isdigit() or int(unitp) < 0:
        flash("Product description is required.")
        error = True
    if not pcategory:
        flash("Product category is required.")
        error = True
    if not pquantity or not pquantity.isdigit() or int(pquantity) < 0:
        flash("Product quantity must be a non-negative integer.")
        error = True
    if not image:
        flash("Product name is required.")
        error = True

    if error:
        return render_template('aProduct.html', pid=pid, pname=pname, pdescription=pdescription, pcategory=pcategory, pquantity=pquantity)
    # Insert operation
    sql = "INSERT INTO ProductProfile (PID, PName, PDescription,UnitPrice, PCategory, Quantity, Image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (pid, pname, pdescription, unitp, pcategory, pquantity,image))
    flash("Product added successfully.")

    dbConn.commit()
    return redirect(url_for('success'))

@app.route('/deleteProduct', methods=['POST'])
def deleteProduct():
    pid = request.form['pid']
    confirm_pid = request.form['confirm_pid']
    verify_delete = request.form.get('verify_delete')  

    if str(pid) != confirm_pid:
        flash("The entered PID does not match.")
        return redirect(url_for('rProduct'))

    if not verify_delete:
        flash("You must confirm the deletion.")
        return redirect(url_for('rProduct'))

    try:
        sql = "DELETE FROM ProductProfile WHERE PID = %s"
        cursor.execute(sql, (pid,))
        dbConn.commit()
        flash("Product removed successfully.")
    except Exception as e:
        dbConn.rollback()
        flash(f"Failed to remove product: {e}")
    return redirect(url_for('rProduct'))

@app.route('/rProduct')
def rProduct():
    sql = "SELECT * FROM ProductProfile"
    cursor.execute(sql)
    products = cursor.fetchall() 
    return render_template('rProduct.html', products=products)



@app.route('/mProduct')
def mProduct():
    sql = "SELECT * FROM ProductProfile"
    cursor.execute(sql)
    products = cursor.fetchall()
    return render_template('mProduct.html', products=products)

@app.route('/modifyProductForm', methods=['POST'])
def modifyProduct():
    pid = request.form.get("pid")
    pname = request.form.get("pname")
    pdescription = request.form.get("pdescription")
    unitp = request.form.get("unitprice")
    pcategory = request.form.get("pcategory")
    pquantity = request.form.get("pquantity")
    image = request.form.get("urlimage")
    verify = request.form.get("verify")

    error = False
    if not verify:
        flash("Box must be checked to verify.")
        error = True

    cursor.execute("SELECT 1 FROM ProductProfile WHERE PID = %s", (pid,))
    if cursor.fetchone() is None:
        flash("No product with this ID exists.")
        error = True

    if not pname:
        flash("Product name is required.")
        error = True
    if not pdescription:
        flash("Product description is required.")
        error = True
    if not unitp or not unitp.isdigit() or int(unitp) < 0:
        flash("Product description is required.")
        error = True
    if not pcategory:
        flash("Product category is required.")
        error = True
    if not pquantity or not pquantity.isdigit() or int(pquantity) < 0:
        flash("Product quantity must be a non-negative integer.")
        error = True
    if not image:
        flash("Product name is required.")
        error = True
    if error:
        return render_template('mProduct.html', pid=pid, pname=pname, pdescription=pdescription, pcategory=pcategory, pquantity=pquantity, unitprice=unitp, urlimage=image)
    
    sql = "UPDATE ProductProfile SET PName = %s, PDescription = %s, UnitPrice = %s, PCategory = %s, Quantity = %s, Image = %s WHERE PID = %s"
    cursor.execute(sql, (pname, pdescription, unitp, pcategory, pquantity, image, pid))
    flash("Product modified successfully.")

    dbConn.commit()
    return redirect(url_for('success'))





@app.route('/sProduct', methods=['GET'])
def sProducts():
    pid = request.args.get('PID')
    pname = request.args.get('PName')

    if pid or pname:
        if pid:
            sql = "SELECT * FROM ProductProfile WHERE PID = %s"
            cursor.execute(sql, (pid,))
        else:
            pname = f"%{pname}%"
            sql = "SELECT * FROM ProductProfile WHERE PName LIKE %s"
            cursor.execute(sql, (pname,))
        products = cursor.fetchall()
        return render_template('search_results_partial.html', products=products)
    else:
        # If no query parameters, render the search form instead
        return render_template('sProduct.html')



@app.route('/Inventory')
def Inventory():
    sql = "SELECT PID as label, Quantity as value FROM ProductProfile"
    cursor.execute(sql)
    inventory_data = cursor.fetchall()

    # Convert the data to JSON format for the chart
    chartData = json.dumps(inventory_data)
    
    return render_template('Inventory.html', chartData=chartData)


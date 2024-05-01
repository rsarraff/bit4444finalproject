# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask  import render_template, request, redirect, url_for, flash, json
from jinja2  import TemplateNotFound

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

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/createShippingRecord')
def createShippingRecord():
    sql = "SELECT OID from Orders"
    cursor.execute(sql)
    orderid = cursor.fetchall()
    return render_template('createShipping.html', orderid=orderid)
        
@app.route('/createShippingForm', methods=['POST'])
def newShippingRecord():

    orderid = request.form.get("orderid")
    vendor = request.form.get("vendor")
    shippingdate = request.form.get("shippingDate")
    shippingstatus = request.form.get("shippingStatus")

    error = False
        
    if not vendor:
        flash("Vendor is required.")
        error = True
    if not shippingdate:
        flash("Shipping Date is required.")
        error = True
    if not shippingstatus:
        flash("Shipping Status is required.")
        error = True

    if error:
        sql = "SELECT OID from Orders"
        cursor.execute(sql)
        orderid = cursor.fetchall()
        return render_template('createShipping.html', orderid=orderid, vendor=vendor, shippingdate=shippingdate, shippingstatus=shippingstatus)

    sql = "INSERT INTO Shipping (OID, Vendor, ShippingDate, ShippingStatus) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql,(orderid, vendor, shippingdate, shippingstatus))
    flash = "Shipping Record Created"

    dbConn.commit()
    return render_template('success.html')

@app.route('/modifyShippingRecord')
def modifyShipping():
    sql = "SELECT SID FROM Shipping"
    cursor.execute(sql)
    shippingid = cursor.fetchall()
    return render_template('modifyShipping.html', shippingid=shippingid)

@app.route('/modifyShippingForm', methods=['POST'])
def modifyShippingForm():
    
    shippingid = request.form.get("shippingid")
    vendor = request.form.get("vendor")
    shippingdate = request.form.get("shippingDate")
    shippingstatus = request.form.get("shippingStatus")
    verify = request.form.get("verify")
    
    error = False

    cursor.execute("SELECT * FROM Shipping WHERE SID = %s", (shippingid,))
    if cursor.fetchone() is None:
        flash("No shipping record with this ID exists.")
        error = True

    if not vendor:
        flash("Vendor is required.")
        error = True
    if not shippingdate:
        flash("Shipping Date is required.")
        error = True
    if not shippingstatus:
        flash("Shipping Status is required.")
        error = True
        
    if not verify:
        flash("Box must be checked to verify.")
        error = True
        
    if error:
        sql = "SELECT SID FROM Shipping"
        cursor.execute(sql)
        shippingid = cursor.fetchall()
        return render_template('modifyShipping.html', shippingid=shippingid, vendor=vendor, shippingdate=shippingdate, shippingstatus=shippingstatus)
    
    sql = "UPDATE Shipping SET Vendor = %s, ShippingDate = %s, ShippingStatus = %s WHERE SID = %s"
    cursor.execute(sql, (vendor, shippingdate, shippingstatus, shippingid))
    flash("Shipping record modified successfully.")

    dbConn.commit()
    return redirect(url_for('success'))

@app.route('/searchShipping', methods=['GET'])
def searchShipping():
    # Get the search query from the request parameter
    searchQuery = request.args.get('searchQuery')
    print(searchQuery)
    if searchQuery:
        # SQL to search both Shipping ID and Order ID
        sql = "SELECT * FROM Shipping WHERE SID = %s OR OID = %s"
        cursor.execute(sql, (searchQuery, searchQuery))
        shippingid = cursor.fetchall()
        print(shippingid)
        
        # Check if any results were found
        if shippingid:
            return render_template('search_results_suppliers.html', shipping=shippingid, searchQuery=searchQuery)
        else:
            return render_template('search_results_suppliers.html', shipping=None, searchQuery=searchQuery)
    else:
        return render_template('searchShipping.html')
    
@app.route('/deleteShipping', methods=['GET', 'POST'])
def deleteShipping():
    SID = request.form.get('SID')  # Update variable name to match form field name
    print("Received input values:")
    print("SID:", SID)  # Update print statement
    
    # input validation
    error = False
    if not SID:
        error = True
        flash("Please input an Shipping ID.")

    if not error:
        # delete the shipping record from the database
        sql = "DELETE FROM Shipping WHERE SID=%s"
        print(cursor.mogrify(sql, (SID,)))
        cursor.execute(sql, (SID,))
        dbConn.commit()
        flash("Shipping record has been deleted!")
        return render_template('success.html')
    else:
        return render_template('deleteShipping.html')

@app.route('/ShippingData')
def shippingData():
    sql = "SELECT ShippingStatus as label, COUNT(*) AS value FROM Shipping GROUP BY ShippingStatus ORDER BY value DESC;"
    cursor.execute(sql)
    vendor_data = cursor.fetchall()

    chartData = json.dumps(vendor_data, default=str) 
    
    return render_template('visuals.html', chartData=chartData)

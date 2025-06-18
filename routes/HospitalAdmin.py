#HospitalAdmin
@app.route('/insert_hospital_admin', methods=['POST'])
def insert_hospital_admin():
    if request.method == 'POST':
        # Process form submission and insert data into the hospital admin table
        
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        contact_number = request.form.get("contact_number")
        email = request.form.get("email")
        address = request.form.get("address")
        role = request.form.get("role")
        
        res = inserthospitaladmin(db, first_name, last_name, contact_number, email, address, role)
        
        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"

    # If the request method is not POST, return an error
    else:
        return "Invalid request method. Please use a POST request."

@app.route('/update_hospital_admin', methods=['POST'])
def update_hospital_admin():
    if request.method == 'POST':
        # Process form submission and update data in the hospital admin table
        admin_id = int(request.form.get("admin_id"))
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        contact_number = request.form.get("contact_number")
        email = request.form.get("email")
        address = request.form.get("address")
        role = request.form.get("role")
        
        
        res = updatehospitaladmin(db, admin_id, first_name, last_name, contact_number, email, address, role)
        
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
        

    

@app.route('/delete_hospital_admin', methods=['POST'])
def delete_hospital_admin():
    if request.method == 'POST':
        # Get the admin ID from the form
        admin_id = int(request.form.get("admin_id"))
        
        # Access the hospital admin collection
        hospital_admin_collection = db['HospitalAdmin']
        
        # Find the admin with the provided ID
        admin = hospital_admin_collection.find_one({"AdminID": admin_id})
        
        if admin:
            # Delete the admin record
            hospital_admin_collection.delete_one({"AdminID": admin_id})
            res = "Hospital admin record deleted successfully."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
        else:
            res = "Hospital admin record not found."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"

#------------------------------------------------------------------------------------------
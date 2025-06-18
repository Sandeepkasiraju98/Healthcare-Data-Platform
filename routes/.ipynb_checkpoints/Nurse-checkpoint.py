#Nurse
@app.route('/insert_nurse', methods=['GET', 'POST'])
def insert_nurse():
    if request.method == 'POST':
        # Process form submission and insert data into the nurse table
        employee_id = int(request.form.get("employee_id"))
        shift = request.form.get("shift")
        qualifications = request.form.get("qualifications")
        
        # Call the insert_nurse method
        res = insertnurse(db, employee_id, shift, qualifications)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
   
    # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('insert_nurse.html')


@app.route('/update_nurse', methods=['POST'])
def update_nurse():
    if request.method == 'POST':
        # Process form submission and update data in the nurse table
        employee_id = int(request.form.get("employee_id"))
        shift = request.form.get("shift")
        qualifications = request.form.get("qualifications")
        
        # Call the update_nurse method
        res = updatenurse(db, employee_id, shift, qualifications)

        # Redirect to the success page after successful update
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"


@app.route('/delete_nurse', methods=['POST'])
def delete_nurse():
    if request.method == 'POST':
        # Get the employee ID from the form
        employee_id = int(request.form.get("employee_id"))
        
        # Access the Nurse collection
        nurse_collection = db['Nurse']
        
        # Find the nurse with the provided ID
        nurse = nurse_collection.find_one({"EmployeeID": employee_id})
        
        if nurse:
            # Delete the nurse record
            nurse_collection.delete_one({"EmployeeID": employee_id})
            res = "Nurse record deleted successfully."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
            
        else:
            res = "Nurse record not found."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
            
#-------------------------------------------------------------------------------------
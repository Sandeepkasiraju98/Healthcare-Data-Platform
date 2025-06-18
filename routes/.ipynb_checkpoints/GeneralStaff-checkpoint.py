#Genereal Staff
@app.route('/insert_general_staff', methods=['GET', 'POST'])
def insert_general_staff():
    if request.method == 'POST':
        # Process form submission and insert data into the general_staff table
        employee_id = int(request.form.get("employee_id"))
        job_description = request.form.get("job_description")
        work_hours = int(request.form.get("work_hours"))
        
        # Call the insert_general_staff method
        res = insertgeneralstaff(db, employee_id, job_description, work_hours)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
   
    # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('insert_general_staff.html')


@app.route('/update_general_staff', methods=['POST'])
def update_general_staff():
    if request.method == 'POST':
        # Process form submission and update data in the general_staff table
        employee_id = int(request.form.get("employee_id"))
        job_description = request.form.get("job_description")
        work_hours = int(request.form.get("work_hours"))
        
        # Call the update_general_staff method
        res = updategeneralstaff(db, employee_id, job_description, work_hours)

        # Redirect to the success page after successful update
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"


@app.route('/delete_general_staff', methods=['POST'])
def delete_general_staff():
    if request.method == 'POST':
        # Get the employee ID from the form
        employee_id = int(request.form.get("employee_id"))
        
        # Access the GeneralStaff collection
        general_staff_collection = db['GeneralStaff']
        
        # Find the general staff with the provided ID
        general_staff = general_staff_collection.find_one({"EmployeeID": employee_id})
        
        if general_staff:
            # Delete the general staff record
            general_staff_collection.delete_one({"EmployeeID": employee_id})
            res = (f"General staff record {employee_id} deleted successfully.")
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
        else:
            res = "General staff record not found."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
            
#------------------------------------------------------------------------------------------
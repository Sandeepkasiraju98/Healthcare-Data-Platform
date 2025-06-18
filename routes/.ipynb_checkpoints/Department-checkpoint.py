#Department
@app.route('/insert_department', methods=['GET', 'POST'])
def insert_department():
    if request.method == 'POST':
        
        # Process form submission and insert data into the department table
        department_name = request.form.get("department_name")
        
        # Call the insert_department method
        res = insertdepartment(db, department_name)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"

   
    # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('insert_department.html')


@app.route('/update_department', methods=['POST'])
def update_department():
    if request.method == 'POST':
        # Process form submission and update data in the department table
        department_number = int(request.form.get("department_number"))
        department_name = request.form.get("department_name")
        
        # Call the update_department method
        res = updatedepartment(db, department_number, department_name)

        # # Redirect to the success page after successful update
        # return res
    
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"



@app.route('/delete_department', methods=['POST'])
def delete_department():
    if request.method == 'POST':
        # Get the department number from the form
        department_number = int(request.form.get("department_number"))
        
        # Access the Department collection
        department_collection = db['Department']
        
        # Find the department with the provided number
        department = department_collection.find_one({"DepartmentNumber": department_number})
        
        if department:
            # Delete the department
            department_collection.delete_one({"DepartmentNumber": department_number})
            return (f"Department {department_number} deleted successfully.")
        else:
            return "Department not found."
#-----------------------------------------------------------------------------------
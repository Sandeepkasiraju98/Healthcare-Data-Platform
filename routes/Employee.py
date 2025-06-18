#Employee
@app.route('/insert_employee', methods=['GET', 'POST'])
def insert_employee():
    if request.method == 'POST':
        # Process form submission and insert data into the employee table
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        position = request.form.get("position")
        department_number = int(request.form.get("department_number"))
        dob = request.form.get("dob")
        contact_number = request.form.get("contact_number")
        email = request.form.get("email")
        address = request.form.get("address")
        hire_date = request.form.get("hire_date")
        salary = float(request.form.get("salary"))
        admin_id = int(request.form.get("admin_id"))
        
        # Call the insert_employee method
        res = insertemployee(db, first_name, last_name, position, department_number, dob, contact_number, email, address, hire_date, salary, admin_id)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
   
    # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('insert_employee.html')

    pass

@app.route('/update_employee', methods=['POST'])
def update_employee():
    if request.method == 'POST':
        # Process form submission and update data in the employee table
        employee_id_str = request.form.get("employee_id")
        employee_id = int(employee_id_str) if employee_id_str.strip() else None
        first_name = request.form.get("first_name") if request.form.get("first_name") is not None else None
        last_name = request.form.get("last_name") if request.form.get("last_name") is not None else None
        position = request.form.get("position") if request.form.get("position") is not None else None
        department_number_str = request.form.get("department_number")
        department_number = int(department_number_str) if department_number_str.strip() else None
        dob = request.form.get("dob") if request.form.get("dob") is not None else None
        contact_number = request.form.get("contact_number") if request.form.get("contact_number") is not None else None
        email = request.form.get("email") if request.form.get("email") is not None else None
        address = request.form.get("address") if request.form.get("address") is not None else None
        hire_date = request.form.get("hire_date") if request.form.get("hire_date") is not None else None
        salary_str = request.form.get("salary")
        salary = float(salary_str) if salary_str.strip() else None
        admin_id_str = request.form.get("admin_id")
        admin_id = int(admin_id_str) if admin_id_str.strip() else None

        
        # Call the update_employee method
        res = updateemployee(db, employee_id, first_name, last_name, position, department_number, dob, contact_number, email, address, hire_date, salary, admin_id)

        # Redirect to the success page after successful update
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"

    
@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    if request.method == 'POST':
        # Get the employee ID from the form
        employee_id = int(request.form.get("employee_id"))
        
        # Access the Employee collection
        employee_collection = db['Employee']
        
        # Find the employee with the provided ID
        employee = employee_collection.find_one({"EmployeeID": employee_id})
        
        if employee:
            # Delete the employee record
            employee_collection.delete_one({"EmployeeID": employee_id})
            res = f"Deleted Employee ID {employee_id}"
             # Redirect to the success page after successful insertion
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
        else:
            return "Employee record not found."

#------------------------------------------------------------------------------------------------
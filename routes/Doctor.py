#Doctor
@app.route('/insert_doctor', methods=['GET', 'POST'])
def insert_doctor():
    if request.method == 'POST':
        # Process form submission and insert data into the doctor table
        employee_id = int(request.form.get("employee_id"))
        specialization = request.form.get("specialization")
        
        # Call the insert_doctor method
        res = insertdoctor(db, employee_id, specialization)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
   
    # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('insert_doctor.html')


@app.route('/update_doctor', methods=['POST'])
def update_doctor():
    if request.method == 'POST':
        # Process form submission and update data in the doctor table
        doctor_id = int(request.form.get("doctor_id"))
        employee_id = int(request.form.get("employee_id"))
        specialization = request.form.get("specialization")
        
        # Call the update_doctor method
        res = updatedoctor(db, doctor_id ,employee_id, specialization)

        # Redirect to the success page after successful update
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"


@app.route('/delete_doctor', methods=['POST'])
def delete_doctor():
    if request.method == 'POST':
        # Get the employee ID from the form
        doctor_id = int(request.form.get("doctor_id"))
        
        # Access the Doctor collection
        doctor_collection = db['Doctor']
        
        # Find the doctor with the provided ID
        doctor = doctor_collection.find_one({"DoctorID": doctor_id})
        
        if doctor:
            # Delete the doctor record
            doctor_collection.delete_one({"DoctorID": doctor_id})
            res = (f"Doctor record {doctor_id} deleted successfully.")
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
        else:
            res = "Doctor record not found."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"


#-------------------------------------------------------------------------------
#Medical Record
@app.route('/insert_medical_record', methods=['GET', 'POST'])
def insert_medical_record():
    if request.method == 'POST':
        # Process form submission and insert data into the medical_records table
        patient_id = int(request.form.get("patient_id"))
        doctor_id = int(request.form.get("doctor_id"))
        visit_date = request.form.get("visit_date")
        diagnosis = request.form.get("diagnosis")
        
        # Call the insert_medical_record method
        res = insertmedicalrecord(db, patient_id, doctor_id, visit_date, diagnosis)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"

   
        # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('insert_medical_record.html')


@app.route('/update_medical_record', methods=['POST'])
def update_medical_record():
    if request.method == 'POST':
        # Process form submission and update data in the medical_records table
      
        patient_id_input = request.form.get("patient_id")
        patient_id = int(patient_id_input.strip()) if patient_id_input.strip() else None
        doctor_id_input = request.form.get("doctor_id")
        doctor_id = int(doctor_id_input.strip()) if doctor_id_input.strip() else None
        visit_date = request.form.get("visit_date")
        diagnosis = request.form.get("diagnosis")
        
        # Call the update_medical_record method
        res = updatemedicalrecord(db, patient_id, doctor_id, visit_date, diagnosis)

        # Redirect to the success page after successful update
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"


@app.route('/delete_medical_record', methods=['POST'])
def delete_medical_record():
    if request.method == 'POST':
        # Get the record ID from the form
        record_id = int(request.form.get("record_id"))
        
        # Access the MedicalRecords collection
        medical_records_collection = db['MedicalRecords']
        
        # Find the medical record with the provided ID
        medical_record = medical_records_collection.find_one({"RecordID": record_id})
        
        if medical_record:
            # Delete the medical record
            medical_records_collection.delete_one({"RecordID": record_id})
            res = "Medical record deleted successfully."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"

        else:
            res = "Medical record not found."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
#------------------------------------------------------------------------------------------
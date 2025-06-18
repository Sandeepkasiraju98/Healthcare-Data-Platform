#Patient----------------------------------------------------------------------------------------
@app.route('/insert_patient', methods=['GET', 'POST'])
def insert_patient():
    if request.method == 'POST':
    
        # Process form submission and insert data into the patient table
        patient_id = int(request.form.get("patient_id"))
        doctor_id = int(request.form.get("doctor_id"))
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        address = request.form.get("address")
        phone = request.form.get("phone")
        email = request.form.get("email")
        emergency_contact_name = request.form.get("emergency_contact_name")
        emergency_contact_phone = request.form.get("emergency_contact_phone")
        insurance_company = request.form.get("insurance_company")
        insurance_policy_number = request.form.get("insurance_policy_number")
        medical_history_summary = request.form.get("medical_history_summary")
        current_medications = request.form.get("current_medications")
        
        # Call the insert_patient method
        res = insertpatient(db,patient_id,doctor_id, first_name, last_name, dob, gender, address, phone, email, emergency_contact_name, emergency_contact_phone, insurance_company, insurance_policy_number, medical_history_summary, current_medications)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
   
    # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('insert_patient.html')

    pass


@app.route('/update_patient', methods=['GET', 'POST'])
def update_patient():
    if request.method == 'POST':
    
        # Process form submission and insert data into the patient table
        patient_id = int(request.form.get("patient_id"))
        doctor_id = int(request.form.get("doctor_id"))
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        address = request.form.get("address")
        phone = request.form.get("phone")
        email = request.form.get("email")
        emergency_contact_name = request.form.get("emergency_contact_name")
        emergency_contact_phone = request.form.get("emergency_contact_phone")
        insurance_company = request.form.get("insurance_company")
        insurance_policy_number = request.form.get("insurance_policy_number")
        medical_history_summary = request.form.get("medical_history_summary")
        current_medications = request.form.get("current_medications")
        
        # Call the insert_patient method
        res = updatepatient(db,patient_id,doctor_id, first_name, last_name, dob, gender, address, phone, email, emergency_contact_name, emergency_contact_phone, insurance_company, insurance_policy_number, medical_history_summary, current_medications)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
   
    # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('update_patient.html')

    pass

@app.route('/delete_patient', methods=['POST'])
def delete_patient():
    if request.method == 'POST':
        # Get the patient ID from the form
        patient_id = int(request.form.get("patient_id"))
        
        # Access the Patient collection
        patient_collection = db['Patient']
        
        # Find the patient with the provided ID
        patient = patient_collection.find_one({"PatientID": patient_id})
        
        if patient:
            # Delete the patient record
            patient_collection.delete_one({"PatientID": patient_id})
            res =  "Patient record deleted successfully."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
        else:
            res = "Patient record not found."
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
#-------------------------------------------------------------------------------------------------------
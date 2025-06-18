@app.route('/schedule_appointment', methods=['GET', 'POST'])
def schedule_appointment():
    if request.method == 'POST':
        
        # Process form submission and insert data into the appointment table
        patient_id = int(request.form.get("patient_id"))
        department_number = int(request.form.get("department_number"))
        datetime_str = request.form.get("datetime")
        date_time = datetime_str
        purpose = request.form.get("purpose")
        
        insert_appointment(patient_id,department_number,date_time,purpose)

        # Redirect to the success page after successful insertion
        return redirect(url_for('success'))
    else:
        # Get the appointment collection
        appointment_collection = db["Appointment"]

        # Get a document from the appointment table to retrieve its keys
        appointment_doc = appointment_collection.find_one()

        if appointment_doc:
            # Get column names from the appointment table excluding "AppointmentID", "ID", and "Status"
            columns = [col for col in appointment_doc.keys() if col not in ["AppointmentID", "_id", "Status"]]
        else:
            columns = []

        # Render the template with column names
        return render_template('schedule_appointment.html', columns=columns)

@app.route('/update_appointment', methods=['POST'])
def update_appointment():
    if request.method == 'POST':
        # Process form submission and update data in the appointment table
        appointment_id = request.form.get("appointment_id")
        patient_id = request.form.get("patient_id")
        doctor_id = request.form.get("doctor_id")
        appointment_date = request.form.get("appointment_date")
        appointment_time = request.form.get("appointment_time")
        
        # Update appointment data in the database
        appointment_collection = db['appointments']
        result = appointment_collection.update_one(
            {"_id": appointment_id},
            {"$set": {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time
            }}
        )
        
        if result.modified_count > 0:
            return "Appointment updated successfully."
        else:
            return "Failed to update appointment. Appointment not found."
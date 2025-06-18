from flask import Flask, render_template, request, redirect, jsonify, url_for, json, flash
import csv
from pymongo import MongoClient
from datetime import datetime
from models.patient import insertpatient, updatepatient
from models.Appointment import insertappointment, updateappointment, process_imported_appointment_data, get_export_data_for_appointment
from models.employee import insertemployee, updateemployee
from models.resource_management import insertresource, updateresource
from models.medical_records import insertmedicalrecord, updatemedicalrecord
from models.nurse import insertnurse, updatenurse
from models.general_staff import insertgeneralstaff, updategeneralstaff
from models.doctor import insertdoctor, updatedoctor, get_doctors_records
from models.department import insertdepartment, updatedepartment
from models.hospital_admin import inserthospitaladmin, updatehospitaladmin

# Initialize Flask app
app = Flask(__name__)
app.secret_key = '9845762145supreethbmohan27'
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['HospitalManagementSystem']

# # Define routes
# @app.route('/')
@app.route('/back_to_update_department')
def redirect_example():
    return render_template('update_department.html')


def export_data_to_csv(data, filename):
    # Write data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Route to render the HTML page
@app.route('/')
def index():
    # Get the list of collection names (tables) from the database
    tables = db.list_collection_names()
    return render_template('index.html', tables=tables)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/importexportjson', methods=['GET', 'POST'])
def importexportjson():
    if request.method == 'POST':
        action = request.form.get('action')
        selected_collection = request.form.get('collection_name')

        if action == 'import':
            import_json_file = request.files.get('import_json')
            if import_json_file:
                import_data = import_json_file.read()
                try:
                    imported_data = json.loads(import_data)
                except json.JSONDecodeError as e:
                    error_message = f"Error decoding JSON file: {str(e)}"
                    return error_message
                
                if selected_collection == 'Appointment':
                    # Process imported data for Appointment collection
                    success = process_imported_appointment_data(imported_data)
                    if success:
                        return (f"Appointment data imported successfully:{success}.")
                    else:
                        return (f"Failed to import Appointment data.")
                elif selected_collection == 'Department':
                    # Process imported data for Department collection
                    success = process_imported_department_data(imported_data)
                    if success:
                        return (f"Department data imported successfully.")
                    else:
                        return (f"Failed to import Department data.")
                # Add more conditions for other collections as needed
                else:
                    return (f"Invalid collection selected.")
            else:
                return (f"No import JSON file provided.")
        
        elif action == 'export':
            if selected_collection == 'Appointment':
                # Get export data for Appointment collection
                export_data = get_export_data_for_appointment()
            elif selected_collection == 'Department':
                # Get export data for Department collection
                export_data = get_export_data_for_department()
            # Add more conditions for other collections as needed
            else:
                return (f"Invalid collection selected.")
            
            if export_data:
                # Define the filename for the CSV file
                filename = f"{selected_collection}_export.csv"

                # Export data to CSV file
                export_data_to_csv(export_data, filename)
                
                # Return the export data as JSON response
                return jsonify(export_data)
            else:
                return (f"No export data available.")
        
            # else:
            #     return (f"Invalid action specified.")

        # # If the method is GET or the action is not recognized, render the same page
        # return render_template('importexportjson.html', collection=selected_collection)
    else:
        collection_names = db.list_collection_names()
        return render_template('/importexportjson.html',collection_names=collection_names)


@app.route('/selectimportexportjson', methods=['GET','POST'])
def selectimportexportjson():
    if request.method == 'POST':
        # Determine the selected collection
        selected_collection = request.form.get('collection_name')
        # Render the HTML page for importing the file
        return render_template('importexportjson.html', collection=selected_collection)
#         
    else:
        collection_names = db.list_collection_names()
        return render_template('/select_collection_json.html',collection_names=collection_names)


@app.route('/select_collection', methods=['GET'])
def select_collection():
    # Get the list of collection names from the database
    collection_names = db.list_collection_names()

    # Render the template with the collection names
    return render_template('select_collection_insert.html', collection_names=collection_names)

@app.route('/doc', methods=['GET', 'POST'])
def doc_record():
    if request.method == 'GET':
        # Assuming you have a function to fetch doctors' records from the database
        doctors = get_doctors_records()

        # Render the template with the list of doctors
        return render_template('/Doctor/Doc.html', doctors=doctors)
    elif request.method == 'POST':
        action = request.form.get('action')
        doctor_id = int(request.form.get('doctor_id'))
        if action == 'update':
            # Get the updated information for the doctor from the form data
            updated_employeeid = int(request.form.get('employee_id'))
            updated_specialization = request.form.get('specialization')
            print(doctor_id,updated_employeeid, updated_specialization)
            # Update the doctor's record in the database
            res = updatedoctor(db,doctor_id,updated_employeeid, updated_specialization)
            result = res.split()[-1]
            return res
            if(result):
                flash('Update successful!', 'success')
                return redirect('/doc')
                
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts) 
                flash('Update Unsuccessful!/n'+res, 'error')
                return redirect('/doc')
                
            # Redirect to the same page to refresh the doctor list
            # return redirect('/doc')
        elif action == 'delete':
            # Delete the doctor's record from the database
            delete_doctor_record(doctor_id)
            # Redirect to the same page to refresh the doctor list
            return redirect('/doc')


# Add more routes for CRUD operations on other collections (Doctor, MedicalRecords, etc.)
@app.route('/insert_record', methods=['GET', 'POST'])
def insert_record():
    if request.method == 'GET':
        # Get the list of collection names from the database
        collection_names = db.list_collection_names()

        # Render the template with the collection names
        return render_template('select_collection_insert.html', collection_names=collection_names)
    else:
        
        # Get the selected collection name from the form data
        collection_name = request.form.get('collection_name')

        # Determine which method to call based on the selected collection
        if collection_name == 'Patient':
            return render_template('Patient/insert_patient.html')
        elif collection_name == 'Employee':
            return render_template('Employee/insert_employee.html')
        elif collection_name == 'Doctor':
            return render_template('Doctor/insert_doctor.html')
        elif collection_name == 'GeneralStaff':
            return render_template('GeneralStaff/insert_general_staff.html')
        elif collection_name == 'Nurse':
            return render_template('Nurse/insert_nurse.html')
        elif collection_name == 'Department':
            return render_template('Department/insert_department.html')
        elif collection_name == 'MedicalRecords':
            return render_template('MedicalRecords/insert_medical_record.html')
        elif collection_name == 'HospitalAdmin':
            return render_template('HospitalAdmin/insert_hospital_admin.html')
        elif collection_name == 'Appointment':
            return render_template('Appointment/schedule_appointment.html')
        elif collection_name == 'ResourceManagement':
            return render_template('ResourceManagement/insert_resource_management.html')
        else:
            return "Invalid collection name"  

        
@app.route('/update_record', methods=['GET', 'POST'])
def update_record():
    if request.method == 'GET':
        # Get the list of collection names from the database
        collection_names = db.list_collection_names()

        # Render the template with the collection names
        return render_template('select_collection_update.html', collection_names=collection_names)
    else:
        
        # Get the selected collection name from the form data
        collection_name = request.form.get('collection_name')

        # Determine which method to call based on the selected collection
        if collection_name == 'Patient':
            return render_template('Patient/update_patient.html')
        elif collection_name == 'Employee':
            return render_template('Employee/update_employee.html')
        elif collection_name == 'Doctor':
            return render_template('Doctor/update_doctor.html')
        elif collection_name == 'GeneralStaff':
            return render_template('GeneralStaff/update_general_staff.html')
        elif collection_name == 'Nurse':
            return render_template('Nurse/update_nurse.html')
        elif collection_name == 'Department':
            return render_template('Department/update_department.html')
        elif collection_name == 'MedicalRecords':
            return render_template('MedicalRecords/update_medical_record.html')
        elif collection_name == 'HospitalAdmin':
            return render_template('HospitalAdmin/update_hospital_admin.html')
        elif collection_name == 'Appointment':
            return render_template('/update_appointment.html')
        elif collection_name == 'ResourceManagement':
            return render_template('ResourceManagement/update_resource_management.html')
        else:
            return "Invalid collection name"        

@app.route('/delete_record', methods=['GET', 'POST'])
def delete_record():
    if request.method == 'GET':
        # Get the list of collection names from the database
        collection_names = db.list_collection_names()

        # Render the template with the collection names
        return render_template('select_collection_delete.html', collection_names=collection_names)
    else:
        
        # Get the selected collection name from the form data
        collection_name = request.form.get('collection_name')

        # Determine which method to call based on the selected collection
        if collection_name == 'Patient':
            return render_template('Patient/delete_patient.html')
        elif collection_name == 'MedicalRecords':
            return render_template('MedicalRecords/delete_medical_record.html')
        elif collection_name == 'Employee':
            return render_template('Employee/delete_employee.html')
        elif collection_name == 'GeneralStaff':
            return render_template('GeneralStaff/delete_general_staff.html')
        elif collection_name == 'Nurse':
            return render_template('Nurse/delete_nurse.html')
        elif collection_name == 'Doctor':
            return render_template('Doctor/delete_doctor.html')
        elif collection_name == 'Department':
            return render_template('Department/delete_department.html')
        elif collection_name == 'HospitalAdmin':
            return render_template('HospitalAdmin/delete_hospital_admin.html')
        elif collection_name == 'ResourceManagement':
            return render_template('ResourceManagement/delete_resource_management.html')
        elif collection_name == 'Appointment':
            return render_template('/delete_appointment.html')
        else:
            return "Invalid collection name" 

#-----------------------------------------------------------------------------------------------------------------

@app.route('/schedule_appointment', methods=['GET', 'POST'])
def schedule_appointment():
    if request.method == 'POST':
        
        # Process form submission and insert data into the appointment table
        patient_id = int(request.form.get("patient_id"))
        department_number = int(request.form.get("department_number"))
        datetime_str = request.form.get("datetime")
        date_time = datetime_str
        purpose = request.form.get("purpose")
        
        res = insertappointment(patient_id,department_number,date_time,purpose)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
    else:
        return render_template('schedule_appointment.html')

@app.route('/update_appointment', methods=['POST'])
def update_appointment():
    if request.method == 'POST':
        # Process form submission and update data in the appointment table
        appointment_id = int(request.form.get("appointment_id"))
        patient_id = int(request.form.get("patient_id"))
        doctor_id = int(request.form.get("doctor_id"))
        appointment_date = request.form.get("appointment_date")
        purpose = request.form.get("purpose")
        status = request.form.get("status")
        
        res = updateappointment(db, appointment_id, patient_id, doctor_id, appointment_date, purpose, status)
        
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"

@app.route('/delete_appointment', methods=['POST'])
def delete_appointment():
    if request.method == 'POST':
        # Get the appointment ID from the form data
        appointment_id = int(request.form.get("appointment_id"))
        
        # Access the Appointment collection
        appointment_collection = db['Appointment']
        
        # Find the appointment with the provided ID
        appointment = appointment_collection.find_one({"AppointmentID": appointment_id})
        
        if appointment:
            # Delete the appointment record
            appointment_collection.delete_one({"AppointmentID": appointment_id})
            return f"Appointment record deleted successfully.<br><br><a href='http://localhost:5000/'>Home</a>"
        else:
            
            return  f"Appointment record not found.<br><br><a href='http://localhost:5000/'>Home</a>"
#-------------------------------------------------
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
#-------------------------------------------------------------------------------------------------------#Resource_Management
@app.route('/insert_resource', methods=['GET', 'POST'])
def insert_resource():
    if request.method == 'POST':
        # Process form submission and insert data into the resource_management table
        resource_type = request.form.get("resource_type")
        resource_name = request.form.get("resource_name")
        status = request.form.get("status")
        location = request.form.get("location")
        admin_id = int(request.form.get("admin_id"))
        
        # Call the insert_resource method
        res = insertresource(db, resource_type, resource_name, status, location, admin_id)

        # Redirect to the success page after successful insertion
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
   
    # If the request method is 'GET', render the HTML page with inputs for the user
    else:
        return render_template('insert_resource.html')


@app.route('/update_resource', methods=['POST'])
def update_resource():
    if request.method == 'POST':
        # Process form submission and insert data into the resource_management table
        resource_id = int(request.form.get("resource_id"))
        resource_type = request.form.get("resource_type")
        resource_name = request.form.get("resource_name")
        status = request.form.get("status")
        location = request.form.get("location")
        admin_id_str = request.form.get("admin_id")
        admin_id = int(admin_id_str) if admin_id_str.strip() else None

        
        # Call the update_resource method
        res = updateresource(db, resource_id, resource_type, resource_name, status, location, admin_id)

        # Redirect to the success page after successful update
        return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"


@app.route('/delete_resource', methods=['POST'])
def delete_resource():
    if request.method == 'POST':
        # Get the resource ID from the form
        resource_id = int(request.form.get("resource_id"))
        
        # Access the Resource Management collection
        resource_collection = db['ResourceManagement']
        
        # Find the resource with the provided ID
        resource = resource_collection.find_one({"ResourceID": resource_id})
        
        if resource:
            # Delete the resource record
            resource_collection.delete_one({"ResourceID": resource_id})
            res = (f"Resource {resource_id} deleted successfully")
            return f"{res}<br><br><a href='http://localhost:5000/'>Home</a>"
        else:
            return "Resource record not found."
#----------------------------------------------------------------------------

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

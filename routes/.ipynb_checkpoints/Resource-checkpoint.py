#Resource_Management
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
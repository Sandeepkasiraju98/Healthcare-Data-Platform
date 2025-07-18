def inserthospitaladmin(db,first_name, last_name, contact_number, email, address, role):
    # Access HospitalAdmin collection
    admin_collection = db['HospitalAdmin']
    
    # Find the last used AdminID, if any
    last_admin = admin_collection.find_one(sort=[("AdminID", -1)])

    # Determine the starting value for AdminID
    start_admin_id = 1 if last_admin is None else last_admin['AdminID'] + 1
    
    # Check if the admin already exists
    existing_admin = admin_collection.find_one({"AdminID": start_admin_id})
    if existing_admin:
        print(f"Admin with ID {start_admin_id} already exists.")
        return (f"Admin with ID {start_admin_id} already exists.")

    # Construct admin data
    admin_data = {
        "AdminID": start_admin_id,
        "FirstName": first_name,
        "LastName": last_name,
        "ContactNumber": contact_number,
        "Email": email,
        "Address": address,
        "Role": role
    }
    
    
    # Insert the data into HospitalAdmin collection
    result = admin_collection.insert_one(admin_data)
    if result:
        print("Inserted ID:", result.inserted_id)
        return (f"Inserted ID: {result.inserted_id}")
    else:
        print("Failed to insert admin.")
        return ("Failed to insert admin.")

def updatehospitaladmin(db, admin_id, first_name, last_name, contact_number, email, address, role):
    # Access HospitalAdmin collection
    admin_collection = db['HospitalAdmin']

    # Check if the admin exists
    existing_admin = admin_collection.find_one({"AdminID": admin_id})
    if not existing_admin:
        print(f"Admin with ID {admin_id} not found.")
        return (f"Admin with ID {admin_id} not found.")

    # Construct update query
    update_query = {}
    if first_name:
        update_query["FirstName"] = first_name
    if last_name:
        update_query["LastName"] = last_name
    if contact_number:
        update_query["ContactNumber"] = contact_number
    if email:
        update_query["Email"] = email
    if address:
        update_query["Address"] = address
    if role:
        update_query["Role"] = role

    # Perform the update
    admin_collection.update_one({"AdminID": admin_id}, {"$set": update_query})
    print(f"Updated record for AdminID {admin_id}")
    return (f"Updated record for AdminID {admin_id}")


def delete_hospital_admin(db, admin_id):
    # Access HospitalAdmin collection
    admin_collection = db['HospitalAdmin']

    # Check if the admin exists
    existing_admin = admin_collection.find_one({"AdminID": admin_id})
    if not existing_admin:
        print(f"Admin with ID {admin_id} not found.")
        return False

    # Delete the admin record
    admin_collection.delete_one({"AdminID": admin_id})
    print(f"Deleted record for AdminID {admin_id}")
    return True

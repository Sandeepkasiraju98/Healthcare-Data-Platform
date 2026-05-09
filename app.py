from flask import Flask, jsonify, request, Response
from pymongo import MongoClient
from etl.etl_pipeline import run_pipeline
import csv
import io
import os

app = Flask(__name__)
app.secret_key = 'healthcare_platform_2024'

# MongoDB connection
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://mongo:27017/'))
db = client['HealthcareDataPlatform']

DATA_FILE = 'healthcare_dataset.csv'

# ─────────────────────────────────────────────
# ETL ROUTE
# ─────────────────────────────────────────────

@app.route('/etl/run', methods=['POST'])
def run_etl():
    """Trigger ETL pipeline to load CSV into MongoDB"""
    try:
        count = run_pipeline(DATA_FILE, db)
        return jsonify({'status': 'success', 'records_loaded': count})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ─────────────────────────────────────────────
# PATIENT ROUTES
# ─────────────────────────────────────────────

@app.route('/patients', methods=['GET'])
def get_patients():
    """Get all patients with optional filters"""
    query = {}
    condition   = request.args.get('condition')
    gender      = request.args.get('gender')
    admission   = request.args.get('admission_type')
    result      = request.args.get('test_result')
    limit       = int(request.args.get('limit', 100))

    if condition: query['Medical Condition'] = condition
    if gender:    query['Gender']            = gender
    if admission: query['Admission Type']    = admission
    if result:    query['Test Results']      = result

    patients = list(db['Patients'].find(query, {'_id': 0}).limit(limit))
    return jsonify({'count': len(patients), 'data': patients})


@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a single patient by ID"""
    patient = db['Patients'].find_one({'PatientID': patient_id}, {'_id': 0})
    if patient:
        return jsonify(patient)
    return jsonify({'error': 'Patient not found'}), 404


@app.route('/patients', methods=['POST'])
def insert_patient():
    """Insert a new patient"""
    data = request.json
    last = db['Patients'].find_one(sort=[('PatientID', -1)])
    data['PatientID'] = (last['PatientID'] + 1) if last else 1
    db['Patients'].insert_one(data)
    data.pop('_id', None)
    return jsonify({'status': 'inserted', 'patient': data}), 201


@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update a patient record"""
    data = request.json
    result = db['Patients'].update_one({'PatientID': patient_id}, {'$set': data})
    if result.matched_count:
        return jsonify({'status': 'updated', 'patient_id': patient_id})
    return jsonify({'error': 'Patient not found'}), 404


@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient record"""
    result = db['Patients'].delete_one({'PatientID': patient_id})
    if result.deleted_count:
        return jsonify({'status': 'deleted', 'patient_id': patient_id})
    return jsonify({'error': 'Patient not found'}), 404


# ─────────────────────────────────────────────
# ANALYTICS ROUTES (for Power BI / dashboards)
# ─────────────────────────────────────────────

@app.route('/analytics/conditions', methods=['GET'])
def conditions_summary():
    """Count of patients per medical condition"""
    pipeline = [
        {'$group': {'_id': '$Medical Condition', 'count': {'$sum': 1},
                    'avg_billing': {'$avg': '$Billing Amount'},
                    'avg_stay': {'$avg': '$Length of Stay'}}},
        {'$sort': {'count': -1}}
    ]
    result = list(db['Patients'].aggregate(pipeline))
    data = []
    for r in result:
        data.append({
            'condition': r['_id'] if r['_id'] else 'Unknown',
            'count': r['count'],
            'avg_billing': round(r['avg_billing'], 2),
            'avg_stay': round(r['avg_stay'], 2)
        })
    return jsonify(data)


@app.route('/analytics/admission_types', methods=['GET'])
def admission_types():
    """Breakdown of admission types"""
    pipeline = [
        {'$group': {'_id': '$Admission Type', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    result = list(db['Patients'].aggregate(pipeline))
    return jsonify([{'type': r['_id'], 'count': r['count']} for r in result])


@app.route('/analytics/insurance', methods=['GET'])
def insurance_summary():
    """Billing stats by insurance provider"""
    pipeline = [
        {'$group': {'_id': '$Insurance Provider',
                    'count': {'$sum': 1},
                    'total_billing': {'$sum': '$Billing Amount'},
                    'avg_billing': {'$avg': '$Billing Amount'}}},
        {'$sort': {'total_billing': -1}}
    ]
    result = list(db['Patients'].aggregate(pipeline))
    return jsonify([{'provider': r['_id'], 'count': r['count'],
                     'total_billing': round(r['total_billing'], 2),
                     'avg_billing': round(r['avg_billing'], 2)} for r in result])


@app.route('/analytics/test_results', methods=['GET'])
def test_results():
    """Breakdown of test results"""
    pipeline = [
        {'$group': {'_id': '$Test Results', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    result = list(db['Patients'].aggregate(pipeline))
    return jsonify([{'result': r['_id'], 'count': r['count']} for r in result])


@app.route('/analytics/monthly_admissions', methods=['GET'])
def monthly_admissions():
    """Monthly admission trends"""
    pipeline = [
        {'$group': {'_id': {'year': '$Admission Year', 'month': '$Admission Month'},
                    'count': {'$sum': 1},
                    'avg_billing': {'$avg': '$Billing Amount'}}},
        {'$sort': {'_id.year': 1}}
    ]
    result = list(db['Patients'].aggregate(pipeline))
    return jsonify([{'year': r['_id']['year'], 'month': r['_id']['month'],
                     'count': r['count'],
                     'avg_billing': round(r['avg_billing'], 2)} for r in result])


@app.route('/analytics/top_doctors', methods=['GET'])
def top_doctors():
    """Top doctors by patient count"""
    pipeline = [
        {'$group': {'_id': '$Doctor', 'patient_count': {'$sum': 1},
                    'avg_billing': {'$avg': '$Billing Amount'}}},
        {'$sort': {'patient_count': -1}},
        {'$limit': 20}
    ]
    result = list(db['Patients'].aggregate(pipeline))
    return jsonify([{'doctor': r['_id'], 'patient_count': r['patient_count'],
                     'avg_billing': round(r['avg_billing'], 2)} for r in result])


# ─────────────────────────────────────────────
# EXPORT ROUTE (for Power BI CSV import)
# ─────────────────────────────────────────────

@app.route('/export/<collection_name>', methods=['GET'])
def export_csv(collection_name):
    """Export any collection as CSV for Power BI"""
    data = list(db[collection_name].find({}, {'_id': 0}))
    if not data:
        return jsonify({'error': 'No data found'}), 404

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename={collection_name}_export.csv'}
    )


# ─────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────

@app.route('/', methods=['GET'])
def health_check():
    collections = db.list_collection_names()
    return jsonify({
        'status': 'running',
        'database': 'HealthcareDataPlatform',
        'collections': collections,
        'endpoints': {
            'etl':       'POST /etl/run',
            'patients':  'GET  /patients',
            'analytics': [
                'GET /analytics/conditions',
                'GET /analytics/admission_types',
                'GET /analytics/insurance',
                'GET /analytics/test_results',
                'GET /analytics/monthly_admissions',
                'GET /analytics/top_doctors'
            ],
            'export': 'GET /export/<collection_name>'
        }
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

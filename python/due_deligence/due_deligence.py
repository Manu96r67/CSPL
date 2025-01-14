from flask import render_template, request, redirect, url_for, flash,jsonify
from python.config import app, db  # Updated import
from python.models import Department, ScreenData


def insert_default_departments():
    if not Department.query.first():  # Check if the table is empty
        default_departments = [
            'Electrical System',
            'Mechanical System',
            'Water and Waste System',
            'Fire Protection System',
            'Building Services and Amenities',
            'Security System'
        ]
        default_departments.sort()
        # Insert each department into the Department table
        for deptname in default_departments:
            new_dept = Department(deptname=deptname)
            db.session.add(new_dept)
        db.session.commit()

@app.route('/due', methods=['GET'])
def indexPage():
    insert_default_departments()  # Your existing function to insert departments
    departments = Department.query.all()
    department_name = request.args.get('deptname', '')
    tabledataId=request.args.get('tabledataId','')
    screen_name = request.args.get('screen_name', '')
    columns = request.args.get('columns', '[]')
    row_data=request.args.get('row_data','[]')

    # Convert columns back from JSON string to a list
    import json
    try:
        columns_list = json.loads(columns)
        row_data=json.loads(row_data)
    except json.JSONDecodeError:
        columns_list = []
    # print('deptname',department_name,'tableid',tabledataId,'screenname',screen_name,'rowdata',row_data,'columns list',columns_list)

    return render_template('due_deligence.html',
                           tabledataId=tabledataId, 
                           departments=departments, 
                           department_name=department_name,
                           screen_name=screen_name,
                           columns=columns_list,
                           row_data=row_data)

@app.route('/edit-table-data', methods=['GET'])
def edit_table_data():
    screen_name = request.args.get('screen_name', None)  
    if screen_name:
        table_data = ScreenData.query.filter_by(screen_name=screen_name).all()
        if not table_data:
            return jsonify({'error': 'No data found for this screen_name'}), 404

        # Prepare data to be sent in the response
        result = {
            'tabledataId':table_data[0].id,
            'deptname': table_data[0].department.deptname,  # Assuming all records are for the same department
            'screen_name': table_data[0].screen_name,
            'columns': table_data[0].columns,
            'row_data': table_data[0].row_data
        }
        # print('result',result);

        return jsonify(result)

    return jsonify({'error': 'screen_name parameter is required'}), 400


@app.route('/submit-table-data', methods=['POST'])
def submit_table_data():
    data = request.json
    print('data is',data)
    screen_name = data.get('screen_name')
    columns = data.get('columns')
    row_data = data.get('row_data')
    deptname = data.get('deptname')
    deptname=deptname.replace('_',' ')

    department = Department.query.filter_by(deptname=deptname).first()
    print('department',deptname)
    if department is None:
        return jsonify({'error': 'Department not found'}, 404)
    
    department_id = department.id
    tabledataId = data.get('tabledataId')  # Get the ID from the request
    print('tableId',tabledataId)
    if tabledataId == "":
        # Try to find the existing entry by ID
        table_entry = ScreenData.query.get(tabledataId)
        if table_entry:
            # Update the existing entry
            table_entry.screen_name = screen_name
            table_entry.columns = columns
            table_entry.row_data = row_data
            table_entry.department_id = department_id
            db.session.commit()
            return jsonify({'redirect': url_for('view_infrastructure')})
        else:
            return jsonify({'error': 'Entry not found'}, 404)
    else:
        print('entered else')
        # Create a new TableData instance
        table_entry = ScreenData(screen_name=screen_name, columns=columns, row_data=row_data, department_id=department_id)
        print('added new entry')
        # Add and commit to the database
        db.session.add(table_entry)
        db.session.commit()
        return jsonify({'redirect': url_for('view_infrastructure')})

@app.route('/get-table-data', methods=['GET'])
def get_table_data():
    all_table_data = (
        db.session.query(ScreenData, Department.deptname)
        .join(Department, ScreenData.department_id == Department.id)
        .all()
    )
    
    tables = []
    for table_data, deptname in all_table_data:
        table_info = {
            'id': table_data.id,
            'department': deptname,  
            'screenName': table_data.screen_name
        }
        tables.append(table_info)
    # print('get-table-data',tables)
    # Return the data as JSON
    return jsonify(tables)

@app.route('/delete-table-data/<int:id>', methods=['DELETE'])
def delete_table_data(id):
    # Find the entry by id
    # print('id is',id)
    entry = ScreenData.query.get(id)
    if entry is None:
        return jsonify({'error': 'Entry not found'}), 404
    
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({'message': 'Entry deleted successfully'}), 200
@app.route('/all-reports')
def view_infrastructure():
    return render_template('view_infrastructure.html')
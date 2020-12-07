import sqlite3
import csv
from sqlite3 import Error
from flask import Flask
from flask import request

app = Flask(__name__)


def create_connection():
    """
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect('db.sqlite')
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)
    return conn


def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute('''create table test_results
                        (
                            device_type TEXT,
                            operator    TEXT,
                            time        datetime,
                            success     TEXT
                    )''')
        with open('test_results.csv', 'r') as person_table:
            rows = csv.DictReader(person_table, )
            to_db = [(row['Device type'], row['Operator'], row['Time'], row['Success']) for row in rows]
        cur.executemany("INSERT INTO test_results VALUES (?,?,?,?);", to_db)
        conn.commit()
    except Error as e:
        print(e)


@app.route('/api_v1/stat', methods=['GET'])
def get_statistics():
    operator = request.args.get('operator')
    if operator:
        conn = create_connection()
        if conn is None:
            return 'Connection lost'
        cur = conn.cursor()
        cur.execute(
            """SELECT device_type,
                   COUNT(case success when 1 then 1 else null end) as success,
                   COUNT(case success when 0 then 1 else null end) as unsuccess
            FROM test_results
            where operator = ?
            group by 1""",
            (operator,))
        rows = cur.fetchall()
        conn.commit()
        result = []
        if not rows:
            return 'result is except by this operator'
        for row in rows:
            result.append({
                'device_type': row['device_type'],
                'success': row['success'],
                'unsuccess': row['unsuccess'],
            })
        return {'result': result}


@app.route('/api_v1/test_result', methods=['POST'])
def add_new_result():
    data = request.form
    device_type = data.get('device_type')
    operator = data.get('operator')
    time = data.get('time')
    success = data.get('success')
    if data:
        conn = create_connection()
        if conn is None:
            return 'Connection lost'
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO test_results(device_type, operator, time, success) VALUES (?, ?, ?, ?)""",
            (device_type, operator, time, success))
        conn.commit()
    return 'add new record'


@app.route('/api_v1/test_result/<int:record_id>', methods=['GET'])
def remove_result(record_id=None):
    conn = create_connection()
    if record_id is None:
        return 'Enter record_id by delete'
    if conn is None:
        return 'Connection lost'
    cur = conn.cursor()
    cur.execute("DELETE FROM test_results WHERE rowid = ?", (record_id,))
    conn.commit()
    return 'delete record'


if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    app.run()

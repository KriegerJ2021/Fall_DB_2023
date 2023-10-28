from flask import Flask, render_template
import util

app = Flask(__name__)

# evil global variables
username='kriegerj21'
password='changeme'
host='127.0.0.1'
port='5432'
database='dvdrental'

@app.route('/')
def index():
    cursor, connection = util.connect_to_db(username, password, host, port, database)
    record = util.run_and_fetch_sql(cursor, "SELECT * from customer;")
    if record == -1:
        print('Something is wrong with the SQL command')
    else:
        col_names = [desc[0] for desc in cursor.description]
        log = record[:5]
    util.disconnect_from_db(connection, cursor)
    return render_template('index.html', sql_table=log, table_title=col_names)

@app.route('/api/update_basket_a')
def update_basket_a():
    cursor, connection = util.connect_to_db(username, password, host, port, database)
    try:
        util.run_sql_command(cursor, "INSERT INTO basket_a VALUES (5, 'Cherry');")
        connection.commit()
        message = "Success!"
    except Exception as e:
        message = str(e)

    util.disconnect_from_db(connection, cursor)
    return message

@app.route('/api/unique')
def show_unique_fruits():
    cursor, connection = util.connect_to_db(username, password, host, port, database)

    try:
        basket_a_unique = util.run_and_fetch_sql(cursor, "SELECT DISTINCT fruit FROM basket_a;")
        basket_b_unique = util.run_and_fetch_sql(cursor, "SELECT DISTINCT fruit FROM basket_b;")
    except Exception as e:
        return str(e)

    util.disconnect_from_db(connection, cursor)
    return render_template('unique_fruits.html', basket_a=basket_a_unique, basket_b=basket_b_unique)

if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)


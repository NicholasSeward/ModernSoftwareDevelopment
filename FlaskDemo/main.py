from flask import Flask
import flask
import sqlite3
import random

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World?'



@app.route('/hello', methods=['GET'])
def hello_name():
    name = flask.request.args.get('name', default='World')
    return f'Hello, {name}!'

@app.route('/storeperson', methods=['POST'])
def store_person():
    # Retrieve name and ssn from the POST request
    name = flask.request.form.get('name', 'Unknown')
    ssn = flask.request.form.get('ssn', '000000000')

    # Connect to the SQLite database
    conn = sqlite3.connect('ssn_data.sqlite')
    cursor = conn.cursor()

    # Insert the new record into the `ssn_data` table
    cursor.execute("INSERT INTO ssn_data (name, ssn_number) VALUES (?, ?)", (name, ssn))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    return flask.redirect('/success')

@app.route('/form', methods=['GET'])
def serve_form():
    return '''
    <form action="/storeperson" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <label for="ssn">SSN:</label>
        <input type="text" id="ssn" name="ssn" required>
        <button type="submit">Submit</button>
    </form>
    '''


@app.route('/success', methods=['GET'])
def success():
    return 'Success! Record has been added.'

@app.route('/peopletable')
def show_people_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('ssn_data.sqlite')
    cursor = conn.cursor()

    # Query all records in the `ssn_data` table
    cursor.execute("SELECT name, ssn_number FROM ssn_data")
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Render the ssn_table.html template with the data
    return flask.render_template("ssn_table.html", data=data)

@app.route('/greet', methods=['GET'])
def greet():
    name = flask.request.args.get('name', default='World')
    return flask.render_template("test.html", name=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)

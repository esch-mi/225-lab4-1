from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # name-based access to columns
    return db


def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT NOT NULL,
                model TEXT NOT NULL
            );
        ''')
        db.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Implements PRG:
      - On POST: perform DB work, then redirect to GET with a message in the query string.
      - On GET: read the message from the query string and render the page.
    """
    if request.method == 'POST':
        # Default message if something unexpected happens
        message = 'OK'

        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            car_id = request.form.get('car_id')
            if car_id:
                db = get_db()
                db.execute('DELETE FROM cars WHERE id = ?', (car_id,))
                db.commit()
                message = 'Car deleted successfully.'
            else:
                message = 'Missing car id.'
            # Redirect to avoid form resubmission on refresh
            return redirect(url_for('index', message=message))

        # Otherwise, it's an add action
        make = request.form.get('make')
        model = request.form.get('model')
        if make and model:
            db = get_db()
            db.execute('INSERT INTO cars (make, model) VALUES (?, ?)', (make, model))
            db.commit()
            message = 'Car added successfully.'
        else:
            message = 'Missing make or model.'

        # Redirect to GET (prevents resubmission on refresh)
        return redirect(url_for('index', message=message))

    # GET request: read optional message from query string
    message = request.args.get('message', '')

    # Always display the cars table
    db = get_db()
    cars = db.execute('SELECT * FROM cars').fetchall()

    # Render page
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cars</title>
        </head>
        <body>
            <h2>Add Car</h2>
            <form method="POST" action="{{ url_for('index') }}">
                <label for="make">Make:</label><br>
                <input type="text" id="make" name="make" required><br>
                <label for="model">Model:</label><br>
                <input type="text" id="model" name="model" required><br><br>
                <input type="submit" value="Submit">
            </form>

            {% if message %}
              <p>{{ message }}</p>
            {% endif %}

            {% if cars %}
                <table border="1" cellpadding="6" cellspacing="0">
                    <tr>
                        <th>Make</th>
                        <th>Model</th>
                        <th>Delete</th>
                    </tr>
                    {% for car in cars %}
                        <tr>
                            <td>{{ car['make'] }}</td>
                            <td>{{ car['model'] }}</td>
                            <td>
                                <form method="POST" action="{{ url_for('index') }}">
                                    <input type="hidden" name="car_id" value="{{ car['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No cars found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, cars=cars)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=False, host='0.0.0.0', port=port)

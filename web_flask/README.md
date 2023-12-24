## Flask Web Framework Overview

### What is a Web Framework?
A web framework is essentially a toolkit that simplifies the process of building web applications. It provides a structure to handle requests, manage routes, and render responses, allowing developers to focus on application logic rather than low-level details.

### Building a Web Framework with Flask
Flask is a lightweight and flexible Python web framework. To start with Flask:

1. **Installation**: Begin by installing Flask via pip:
    ```bash
    pip install Flask
    ```

2. **Basic App Structure**: A minimal Flask app looks like this:
    ```python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello, Flask!'
    ```

3. **Running the App**: Execute the app using:
    ```bash
    flask run
    ```

## Working with Routes and Templates in Flask

### Routes in Flask
In Flask, a route associates a URL with a specific function in your application. It defines how the app responds to different HTTP requests.

### Route Definition
Example of defining routes in Flask:
```python
@app.route('/about')
def about():
    return 'This is the About page'
```

### Handling Variables in Routes
Flask allows passing variables in routes:
```python
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'
```

### Templates in Flask
Templates in Flask are HTML files that allow you to separate the presentation layer from your Python code.

### Creating HTML Response with Templates
1. **Render Template**:
    ```python
    from flask import render_template

    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)
    ```

2. **HTML Template Example** (`hello.html`):
    ```html
    <html>
    <head><title>Greetings</title></head>
    <body>
        <h1>Hello, {{ name }}!</h1>
    </body>
    </html>
    ```

### Dynamic Templates in Flask
Flask templates support loops, conditions, and other control structures to create dynamic content.

### Displaying Data from MySQL Database in HTML
1. **Connecting to MySQL**:
   Use libraries like `Flask-MySQLdb` to connect Flask to MySQL.

2. **Querying Data**:
   Fetch data from the database using SQLAlchemy or similar libraries and pass it to your template for display.

3. **Example**:
    ```python
    @app.route('/users')
    def show_users():
        # Assuming `users` is a list of dictionaries fetched from the database
        users = [
            {'username': 'Alice', 'email': 'alice@example.com'},
            {'username': 'Bob', 'email': 'bob@example.com'}
        ]
        return render_template('users.html', users=users)
    ```

4. **HTML Template Example** (`users.html`):
    ```html
    <html>
    <head><title>User List</title></head>
    <body>
        <h1>User List</h1>
        <ul>
            {% for user in users %}
                <li>{{ user.username }} - {{ user.email }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    ```

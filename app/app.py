from flask import Flask, request, render_template_string, redirect
import os
from models import ItemModel

app = Flask(__name__)
model = ItemModel()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Todo List</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input { padding: 8px; margin-right: 10px; width: 250px; }
        button { padding: 8px 20px; cursor: pointer; }
        ul { margin-top: 20px; list-style: none; padding: 0; }
        li { padding: 8px; margin: 5px 0; background: #f4f4f4; border-radius: 4px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Todo List</h1>
    <form method="post">
        <input type="text" name="task" placeholder="Enter new task" required>
        <button type="submit">Add Task</button>
    </form>
    {% if items %}
        <ul>
        {% for item in items %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No tasks yet. Add one above!</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        if task:
            # Добавление задачи через модель
            conn = model.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO items (name) VALUES (%s)', (task,))
            conn.commit()
            cursor.close()
            conn.close()
        return redirect('/')
    
    items = model.get_all_items()
    return render_template_string(HTML, items=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, redirect, render_template_string, request, url_for

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "tasks.db")

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Student Task Tracker</title>
  <style>
    body{font-family:Arial,sans-serif;background:#f3f6fb;margin:0;color:#172033}
    main{max-width:760px;margin:40px auto;padding:24px;background:white;border-radius:14px;box-shadow:0 8px 30px #17203314}
    h1{margin-top:0} form.add{display:flex;gap:8px;margin:22px 0}
    input{flex:1;padding:12px;border:1px solid #ccd4e0;border-radius:8px}
    button{padding:11px 15px;border:0;border-radius:8px;background:#2457d6;color:white;cursor:pointer}
    ul{list-style:none;padding:0} li{display:flex;align-items:center;gap:12px;padding:13px 4px;border-bottom:1px solid #edf0f5}
    li.done span{text-decoration:line-through;color:#7a8495}.task{flex:1}
    .inline{display:inline}.delete{background:#b42318}.meta{color:#687386;font-size:13px}
    a{color:#2457d6}
  </style>
</head>
<body><main>
  <h1>Student Task Tracker</h1>
  <p>Demo application: add tasks, mark them complete, and delete them.</p>
  <form class="add" method="post" action="/tasks">
    <input name="title" placeholder="e.g. Complete Python assignment" required maxlength="120">
    <button type="submit">Add task</button>
  </form>
  <ul>
  {% for task in tasks %}
    <li class="{{ 'done' if task['done'] else '' }}">
      <form class="inline" method="post" action="/tasks/{{task['id']}}/toggle">
        <button type="submit">{{ 'Undo' if task['done'] else 'Done' }}</button>
      </form>
      <span class="task">{{ task['title'] }}</span>
      <form class="inline" method="post" action="/tasks/{{task['id']}}/delete">
        <button class="delete" type="submit">Delete</button>
      </form>
    </li>
  {% else %}
    <li>No tasks yet. Add your first task above.</li>
  {% endfor %}
  </ul>
  <p class="meta">Application status: <a href="/health">health</a> · <a href="/api/tasks">JSON API</a></p>
</main></body></html>
"""

def get_db():
    path = Path(DB_PATH)
    if str(path.parent) not in ("", "."):
        path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)

@app.get("/")
def home():
    with get_db() as conn:
        tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return render_template_string(PAGE, tasks=tasks)

@app.post("/tasks")
def add_task():
    title = request.form.get("title", "").strip()
    if not title:
        return "Task title is required", 400
    with get_db() as conn:
        conn.execute("INSERT INTO tasks(title) VALUES (?)", (title,))
    return redirect(url_for("home"))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    with get_db() as conn:
        conn.execute("UPDATE tasks SET done = CASE done WHEN 0 THEN 1 ELSE 0 END WHERE id = ?", (task_id,))
    return redirect(url_for("home"))

@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    with get_db() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("home"))

@app.get("/api/tasks")
def api_tasks():
    with get_db() as conn:
        tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return jsonify([dict(task) for task in tasks])

@app.get("/health")
def health():
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="healthy"), 200
    except sqlite3.Error:
        return jsonify(status="unhealthy"), 503

@app.get("/live")
def live():
    return jsonify(status="alive"), 200

@app.get("/ready")
def ready():
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="ready"), 200
    except sqlite3.Error:
        return jsonify(status="not-ready"), 503

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))

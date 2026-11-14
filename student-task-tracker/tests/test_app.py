import app as app_module

def configure_test_db(tmp_path):
    app_module.app.config["TESTING"] = True
    app_module.DB_PATH = str(tmp_path / "test.db")
    app_module.init_db()

def test_home_page(tmp_path):
    configure_test_db(tmp_path)
    response = app_module.app.test_client().get("/")
    assert response.status_code == 200
    assert b"Student Task Tracker" in response.data

def test_health_endpoints(tmp_path):
    configure_test_db(tmp_path)
    client = app_module.app.test_client()
    assert client.get("/health").status_code == 200
    assert client.get("/live").status_code == 200
    assert client.get("/ready").status_code == 200

def test_add_task_and_api(tmp_path):
    configure_test_db(tmp_path)
    client = app_module.app.test_client()
    response = client.post("/tasks", data={"title": "Learn Docker"})
    assert response.status_code == 302
    tasks = client.get("/api/tasks").get_json()
    assert any(task["title"] == "Learn Docker" for task in tasks)

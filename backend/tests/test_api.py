import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_upload_and_query(tmp_path):
    file_path = tmp_path / "test.md"
    file_path.write_text("# Title\nHello")
    with open(file_path, "rb") as f:
        resp = client.post("/upload", files={"file": ("test.md", f, "text/markdown")})
        assert resp.status_code == 200
    resp = client.post("/query", data={"q": "Hello"})
    assert resp.status_code == 200
    assert "results" in resp.json()

# tests/conftest.py
import os, threading, time, urllib.request, contextlib
import pytest
from werkzeug.serving import make_server
from app.app import app  # adjust if your import path differs

HOST = "127.0.0.1"
PORT = 15000
BASE_URL = f"http://{HOST}:{PORT}"

class ServerThread(threading.Thread):
    def __init__(self, app, host, port):
        super().__init__(daemon=True)
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()
    def run(self):
        self.server.serve_forever()
    def shutdown(self):
        self.server.shutdown()
        self.ctx.pop()

def _wait_for(url, timeout=10.0):
    start = time.time(); last_err = None
    while time.time() - start < timeout:
        try:
            with contextlib.closing(urllib.request.urlopen(url, timeout=1.0)):
                return
        except Exception as e:
            last_err = e
            time.sleep(0.1)
    raise RuntimeError(f"Server not reachable at {url}. Last error: {last_err}")

@pytest.fixture(scope="session", autouse=True)
def start_server():
    os.environ.setdefault("PYTEST_CURRENT_TEST", "1")  # let app know we're testing
    app.config["WTF_CSRF_ENABLED"] = False            # disable CSRF in tests

    server = ServerThread(app, HOST, PORT)
    server.start()

    # wait until the page responds (root or /calculadora)
    try:
        _wait_for(f"{BASE_URL}/")
    except RuntimeError:
        print("Server failed to start")

    yield
    server.shutdown()


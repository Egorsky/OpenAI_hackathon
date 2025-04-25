"""
Dev launcher: `python run.py` starts uvicorn with hot-reload.
Prod: gunicorn -k uvicorn.workers.UvicornWorker -w 4 app:app  :contentReference[oaicite:5]{index=5}
"""

import os, uvicorn
from back_app import app

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    reload_flag = os.getenv("UVICORN_RELOAD", "true").lower() == "true"

    # Pass an *import string* when reload is on, otherwise pass the object
    if reload_flag:
        uvicorn.run("app:app", host=host, port=port, reload=True)  # ← import string
    else:
        from app import app
        uvicorn.run(app, host=host, port=port)
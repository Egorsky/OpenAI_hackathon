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

    # ALWAYS use an import string so reload & workers work
    uvicorn.run("back_app:app", host=host, port=port, reload=reload_flag)
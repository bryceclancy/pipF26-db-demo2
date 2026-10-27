import os

from dotenv import load_dotenv
from flask import Flask, render_template
import psycopg

load_dotenv()

app = Flask(__name__)


def get_connection():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    if "sslmode=" not in url:
        url += ("&" if "?" in url else "?") + "sslmode=require"
    return psycopg.connect(url)


@app.route("/")
def index():
    with get_connection() as conn:
        students = conn.execute(
            "SELECT name FROM students ORDER BY name"
        ).fetchall()
    names = [row[0] for row in students]
    return render_template("index.html", names=names)


if __name__ == "__main__":
    app.run(debug=True)

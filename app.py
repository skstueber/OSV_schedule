from flask import Flask, render_template
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

DATA_DIR = "data"

def parse_date_from_filename(filename):
    try:
        base = os.path.splitext(filename)[0]  # remove .csv
        date_str = base.replace("schedule-", "")
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None

def load_schedules():
    schedules = []
    now = datetime.now()

    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".csv"):
            continue

        start_date = parse_date_from_filename(fname)
        if not start_date:
            continue

        end_date = start_date + pd.Timedelta(days=13)

        # delete expired schedules
        if end_date < now:
            os.remove(os.path.join(DATA_DIR, fname))
            continue

        df = pd.read_csv(os.path.join(DATA_DIR, fname))
        week_range = f"{start_date.strftime('%b %d, %Y')} – {end_date.strftime('%b %d, %Y')}"
        schedules.append({
            "start": start_date,
            "end": end_date,
            "week_range": week_range,
            "data": df.to_dict(orient="records"),
            "columns": list(df.columns)
        })

    # sort schedules by start date
    schedules.sort(key=lambda s: s["start"])
    return schedules

@app.route("/")
def index():
    schedules = load_schedules()
    return render_template("schedule.html", schedules=schedules)


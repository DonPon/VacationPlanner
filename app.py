from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

HOLIDAYS = [
    "2026-01-01","2026-01-02","2026-04-03","2026-04-06","2026-05-01",
    "2026-05-14","2026-05-25","2026-08-01","2026-09-14","2026-12-25","2026-12-26"
]
HOLIDAYS = [datetime.strptime(d, "%Y-%m-%d").date() for d in HOLIDAYS]

blocks_franz = [
    {"name":"Easter/Mexico", "holiday":"(2026-04-03, 2026-04-06)", "start":"2026-03-28", "used":11},
    {"name":"Ascension", "holiday":"(2026-05-14)", "start":"2026-05-15", "used":1},
    {"name":"Pentecost", "holiday":"(2026-05-25)", "start":"2026-05-26", "used":4},
    {"name":"Autumn/Knabenschiessen", "holiday":"(2026-09-14)", "start":"2026-09-15", "used":4},
    {"name":"Christmas", "holiday":"(2026-12-25, 2026-12-26)", "start":"2026-12-19", "used":4},
]

blocks_polina = [
    {"name":"Easter/Mexico", "holiday":"(2026-04-03, 2026-04-06)", "start":"2026-03-28", "used":7},
    {"name":"Ascension", "holiday":"(2026-05-14)", "start":"2026-05-15", "used":1},
    {"name":"Pentecost", "holiday":"(2026-05-25)", "start":"2026-05-26", "used":4},
    {"name":"Autumn/Knabenschiessen", "holiday":"(2026-09-14)", "start":"2026-09-15", "used":4},
    {"name":"Christmas", "holiday":"(2026-12-25, 2026-12-26)", "start":"2026-12-19", "used":4},
]

def count_workdays(start_date, end_date):
    count = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5 and current not in HOLIDAYS:
            count += 1
        current += timedelta(days=1)
    return count

def add_workdays(start_date, workdays):
    current = start_date
    days_added = 0
    while days_added < workdays:
        current += timedelta(days=1)
        if current.weekday() < 5 and current not in HOLIDAYS:
            days_added += 1
    return current

def calculate_blocks(blocks):
    result = []
    for block in blocks:
        if not block.get("start"):
            continue
        start = datetime.strptime(block["start"], "%Y-%m-%d").date()

        if "end_date_str" in block and block["end_date_str"]:
            end = datetime.strptime(block["end_date_str"], "%Y-%m-%d").date()
            used = count_workdays(start, end)
        else:
            used = block["used"]
            end = add_workdays(start, used)

        total_days_off = (end - start).days + 1

        # Expansión de viaje
        trip_start = start
        trip_end = end
        # Si inicia en lunes, sugerir viaje desde sábado anterior
        if start.weekday() == 0:
            trip_start = start - timedelta(days=2)
        # Si termina en viernes, sugerir viaje hasta domingo siguiente
        if end.weekday() == 4:
            trip_end = end + timedelta(days=2)

        result.append({
            "name": block["name"],
            "start_iso": block["start"],
            "start": start.strftime("%d-%b-%Y"),
            "used": used,
            "end": end.strftime("%d-%b-%Y"),
            "end_iso": end.strftime("%Y-%m-%d"),
            "total_days_off": total_days_off,
            "trip_start": trip_start.strftime("%d-%b-%Y"),
            "trip_end": trip_end.strftime("%d-%b-%Y"),
            "trip_total_days": (trip_end - trip_start).days + 1,
            "holiday": block.get("holiday", ""),  # Use .get() to provide a default value
        })
    return result

@app.route("/")
def index():
    vacation_days_allowed_franz = 25
    vacation_days_allowed_polina = 22

    calc_franz = calculate_blocks(blocks_franz)
    calc_polina = calculate_blocks(blocks_polina)

    vacation_days_remaining_franz = vacation_days_allowed_franz - sum(b["used"] for b in blocks_franz)
    vacation_days_remaining_polina = vacation_days_allowed_polina - sum(b["used"] for b in blocks_polina)

    return render_template("index.html",
                           blocks_franz=calc_franz,
                           blocks_polina=calc_polina,
                           vacation_days_allowed_franz=vacation_days_allowed_franz,
                           vacation_days_allowed_polina=vacation_days_allowed_polina,
                           vacation_days_remaining_franz=vacation_days_remaining_franz,
                           vacation_days_remaining_polina=vacation_days_remaining_polina)

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    vacation_days_allowed_franz = data.get("vacation_days_allowed_franz", 25)
    vacation_days_allowed_polina = data.get("vacation_days_allowed_polina", 22)
    updated_franz_blocks = []
    for block in data.get("blocks_franz", []) :
        if block.get("start"):
            updated_franz_blocks.append({"name": block["name"], "start": block["start"], "end_date_str": block["end_date_str"]})

    updated_polina_blocks = []
    for block in data.get("blocks_polina", []) :
        if block.get("start"):
            updated_polina_blocks.append({"name": block["name"], "start": block["start"], "end_date_str": block["end_date_str"]})

    calc_franz = calculate_blocks(updated_franz_blocks)
    calc_polina = calculate_blocks(updated_polina_blocks)

    remaining_franz = vacation_days_allowed_franz - sum(b["used"] for b in calc_franz)
    remaining_polina = vacation_days_allowed_polina - sum(b["used"] for b in calc_polina)

    return jsonify({
        "blocks_franz": calc_franz,
        "blocks_polina": calc_polina,
        "remaining_franz": remaining_franz,
        "remaining_polina": remaining_polina
    })

if __name__ == "__main__":
    app.run(debug=True)

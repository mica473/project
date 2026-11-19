from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

def load_museums():
    # Lecture du fichier CSV
    csv_path = os.path.join(os.path.dirname(__file__), "data", "musees.csv")
    museums = []

    with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            museums.append({
                "name": row["Name"].strip(),
                "arrondissement": int(row["Arrondissement"]),
                "themes": [theme.strip() for theme in row["Themes"].split(",")],
                "pmr": row["PMR"].strip(),
                "nocturnes": row["Nocturnes"].strip(),
                "latitude": float(row["Latitude"]),
                "longitude": float(row["Longitude"])
            })

    return museums

def filter_museums(museums):

    arrondissement = request.args.get("arrondissement", "")
    selected_themes = request.args.get("theme","")
    pmr = request.args.get("pmr", "")
    nocturnes = request.args.get("nocturnes", "")

    filtered = []

    for museum in museums:

        if arrondissement and str(museum["arrondissement"]) != arrondissement:
            continue

        if selected_themes and selected_themes not in museum["themes"]:
            continue

        if pmr and museum["pmr"] != pmr:
            continue

        if nocturnes and museum["nocturnes"] != nocturnes:
            continue

        filtered.append(museum)

    return filtered

@app.get("/")
def index():

    museums = load_museums()
    filtered = filter_museums(museums)

    return render_template(
        "index.html",
        museums=filtered,
        museums_for_map=filtered,
        arrondissements=sorted({museum["arrondissement"] for museum in museums}),
        themes=sorted({theme for museum in museums for theme in museum["themes"]}),
        selected_arrondissement=request.args.get("arrondissement", ""),
        selected_themes=request.args.get("theme", ""),
        selected_pmr=request.args.get("pmr", ""),
        selected_nocturnes=request.args.get("nocturnes", ""),
        total=len(museums)
    )


if __name__ == "__main__":
    app.run()
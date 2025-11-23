import copy
import os
from flask import Flask, request, redirect, send_file
from core import FpiClient, search, write_to_excel

HOSTNAME = "127.0.0.1"
PORT = 5000
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

app = Flask(
    __name__,
    static_folder="../client",
    static_url_path="",
    template_folder="../client"
)

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

fpi_client = FpiClient()
current_file = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            comitato = request.form.get("comitato", "")
            qualifica = request.form.get("qualifica", "")
            peso = request.form.get("peso", "")
            min_matches = request.form.get("min_matches", "")
            max_matches = request.form.get("max_matches", "")
            filename = request.form.get("filename", "")

            if not qualifica:
                return redirect("/?error=1")

            if not filename:
                return redirect("/?error=2")

            min_val = 0
            if min_matches:
                if not min_matches.isdigit() or len(min_matches) > 3:
                    return redirect("/?error=3")
                min_val = int(min_matches)
                if min_val > 999:
                    return redirect("/?error=3")

            max_val = 999
            if max_matches:
                if not max_matches.isdigit() or len(max_matches) > 3:
                    return redirect("/?error=4")
                max_val = int(max_matches)
                if max_val > 999:
                    return redirect("/?error=4")

            if min_val > max_val:
                return redirect("/?error=5")

            fpi_client.update_comitato(comitato if comitato else None)
            fpi_client.update_qualifiche(qualifica)
            fpi_client.update_pesi(peso if peso else None)

            client_copy = copy.deepcopy(fpi_client)
            athletes = search(client_copy, min_val, max_val)

            if not athletes:
                return redirect("/?error=6")

            filepath = os.path.join(DOWNLOAD_FOLDER, f"{filename}.xlsx")
            write_to_excel(athletes, filepath)

            global current_file
            current_file = filepath

            return redirect("/?success=1")

        except Exception as e:
            print(f"Errore durante la ricerca: {e}")
            return redirect("/?error=7")

    return app.send_static_file("index.html")


@app.route("/download")
def download():
    global current_file

    if not current_file or not os.path.exists(current_file):
        return redirect("/?error=8")

    try:
        return send_file(
            current_file,
            as_attachment=True,
            download_name=os.path.basename(current_file),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(f"Errore durante il download: {e}")
        return redirect("/?error=7")


@app.route("/api/qualifiche")
def fetchQualifiche():
    try:
        html = fpi_client.qualifiche_html()
        return html, 200
    except Exception as e:
        print(f"Errore fetchQualifiche: {e}")
        return redirect("/?error=9")


@app.route("/api/pesi")
def fetchPesi():
    try:
        html = fpi_client.pesi_html()
        return html, 200
    except RuntimeError as e:
        print(f"Errore fetchPesi (runtime): {e}")
        return redirect("/?error=9")
    except Exception as e:
        print(f"Errore fetchPesi: {e}")
        return redirect("/?error=9")


@app.route("/api/update/comitato/<int:id>")
def updateComitato(id):
    try:
        fpi_client.update_comitato(str(id) if id else None)
        return "", 204
    except Exception as e:
        print(f"Errore updateComitato: {e}")
        return redirect("/?error=9")


@app.route("/api/update/qualifica/<int:id>")
def updateQualifica(id):
    try:
        fpi_client.update_qualifiche(str(id) if id else None)
        return "", 204
    except Exception as e:
        print(f"Errore updateQualifica: {e}")
        return redirect("/?error=9")


@app.route("/api/update/peso/<int:id>")
def updatePeso(id):
    try:
        fpi_client.update_pesi(str(id) if id else None)
        return "", 204
    except Exception as e:
        print(f"Errore updatePeso: {e}")
        return redirect("/?error=9")


if __name__ == "__main__":
    app.run(debug=True, port=PORT, host=HOSTNAME)
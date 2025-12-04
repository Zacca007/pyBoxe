import copy
import os
from datetime import timedelta
from flask import Flask, request, redirect, send_file, session
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

# Configurazione sessioni Flask
app.secret_key = os.urandom(24)  # Chiave segreta per crittografare le sessioni
app.config['SESSION_TYPE'] = 'filesystem'  # Opzionale: per sessioni persistenti
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Durata sessione: 1 ora
app.config['SESSION_COOKIE_SECURE'] = False  # Impostare True in produzione con HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Dizionario per memorizzare i client FPI per ogni sessione
session_clients = {}


def get_or_create_client():
    """
    Ottiene il client FPI per la sessione corrente o ne crea uno nuovo.
    """
    session_id = session.get('sid')

    # Se non esiste un session_id, creane uno
    if not session_id:
        session_id = os.urandom(16).hex()
        session['sid'] = session_id
        session.permanent = True  # Rende la sessione permanente (usa PERMANENT_SESSION_LIFETIME)

    # Se il client non esiste per questa sessione, crealo
    if session_id not in session_clients:
        session_clients[session_id] = FpiClient()

    return session_clients[session_id]


def cleanup_old_sessions():
    """
    Rimuove le sessioni inattive (chiamare periodicamente o all'avvio).
    In questo caso semplificato, manteniamo un numero massimo di sessioni.
    """
    MAX_SESSIONS = 100
    if len(session_clients) > MAX_SESSIONS:
        # Rimuovi le prime 20 sessioni (FIFO)
        sessions_to_remove = list(session_clients.keys())[:20]
        for sid in sessions_to_remove:
            del session_clients[sid]


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

            # Ottieni il client per questa sessione
            fpi_client = get_or_create_client()

            fpi_client.update_comitato(comitato if comitato else None)
            fpi_client.update_qualifiche(qualifica)
            fpi_client.update_pesi(peso if peso else None)

            client_copy = copy.deepcopy(fpi_client)
            athletes = search(client_copy, min_val, max_val)

            if not athletes:
                return redirect("/?error=6")

            filepath = os.path.join(DOWNLOAD_FOLDER, f"{filename}.xlsx")
            write_to_excel(athletes, filepath)

            # Salva il percorso del file nella sessione
            session['last_file'] = filepath

            return redirect("/?success=1")

        except Exception as e:
            print(f"Errore durante la ricerca: {e}")
            return redirect("/?error=7")

    return app.send_static_file("index.html")


@app.route("/download")
def download():
    # Recupera il file dalla sessione
    filepath = session.get('last_file')

    if not filepath or not os.path.exists(filepath):
        return redirect("/?error=8")

    try:
        return send_file(
            filepath,
            as_attachment=True,
            download_name=os.path.basename(filepath),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(f"Errore durante il download: {e}")
        return redirect("/?error=7")


@app.route("/api/qualifiche")
def fetchQualifiche():
    try:
        fpi_client = get_or_create_client()
        html = fpi_client.qualifiche_html()
        return html, 200
    except Exception as e:
        print(f"Errore fetchQualifiche: {e}")
        return redirect("/?error=9")


@app.route("/api/pesi")
def fetchPesi():
    try:
        fpi_client = get_or_create_client()
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
        fpi_client = get_or_create_client()
        fpi_client.update_comitato(str(id) if id else None)
        return "", 204
    except Exception as e:
        print(f"Errore updateComitato: {e}")
        return redirect("/?error=9")


@app.route("/api/update/qualifica/<int:id>")
def updateQualifica(id):
    try:
        fpi_client = get_or_create_client()
        fpi_client.update_qualifiche(str(id) if id else None)
        return "", 204
    except Exception as e:
        print(f"Errore updateQualifica: {e}")
        return redirect("/?error=9")


@app.route("/api/update/peso/<int:id>")
def updatePeso(id):
    try:
        fpi_client = get_or_create_client()
        fpi_client.update_pesi(str(id) if id else None)
        return "", 204
    except Exception as e:
        print(f"Errore updatePeso: {e}")
        return redirect("/?error=9")


@app.before_request
def before_request():
    """Eseguito prima di ogni richiesta - utile per pulizia periodica"""
    cleanup_old_sessions()


if __name__ == "__main__":
    print("✅ Server PyBoxe attivo su http://127.0.0.1:5000")
    app.run(debug=True, port=PORT, host=HOSTNAME)
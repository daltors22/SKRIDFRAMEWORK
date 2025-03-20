from flask import Blueprint, send_from_directory, abort
import os

files_routes = Blueprint("files", __name__)

# Définir DATA_FOLDER de manière relative au fichier actuel :
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# 📂 Servir les fichiers statiques depuis `/backend/data/`
@files_routes.route("/data/<author>/<subfolder>/<filename>", methods=["GET"])
def serve_file(author, subfolder, filename):
    """
    📌 Servir un fichier SVG ou MEI depuis /backend/data/author/subfolder/ (par exemple, svg ou mei)
    """
    data_folder = os.path.join(DATA_FOLDER, author, subfolder)
    file_path = os.path.join(data_folder, filename)

    print(f"🔍 Requête pour {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ Fichier introuvable : {file_path}")
        return abort(404)

    print(f"✅ Fichier trouvé, envoi : {file_path}")
    return send_from_directory(data_folder, filename)

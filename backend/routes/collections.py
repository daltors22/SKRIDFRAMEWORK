from flask import Blueprint, request, jsonify
from ..database import driver  # ✅ Connexion à Neo4j
import os

collections_routes = Blueprint("collections", __name__)  # ✅ Nom correct du Blueprint

#DATA_PATH = os.path.join(os.getcwd(), "data")  # 📂 `/backend/data/`
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

@collections_routes.route("/", methods=["GET"])
def get_collections():
    try:
        print("🟢 Query String :", request.args)
        print("🟢 JSON Body :", request.get_json(silent=True))

        query = "MATCH (s:Score) RETURN DISTINCT s.collection"
        with driver.session() as session:
            result = session.run(query)
            authors = [record["s.collection"] for record in result]

        response = jsonify({"authors": authors})
        response.headers["Content-Type"] = "application/json"
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as e:
        print(f"❌ Erreur /collections: {e}")
        return jsonify({"error": str(e)}), 500


@collections_routes.route("/getCollectionByAuthor", methods=["GET"])
def get_collection_by_author():
    author = request.args.get("author")
    if not author:
        return jsonify({"error": "Author parameter is required"}), 400

    # 🔥 Corrige le chemin pour gérer les espaces et normaliser
    author_folder = os.path.normpath(os.path.join(DATA_PATH, author, "svg"))

    if not os.path.exists(author_folder):
        return jsonify({"error": f"Author SVG folder not found: {author_folder}"}), 404

    # Récupérer tous les fichiers SVG
    svg_files = [
        {"collection": author, "source": f"/data/{author}/svg/{file}"}
        for file in os.listdir(author_folder)
        if file.endswith(".svg")  # 🔥 On ne récupère que les SVG
    ]
    print("🔵 Route /collections/getCollectionByAuthor enregistrée !")

    return jsonify({"results": svg_files})

from flask import Blueprint, request, jsonify
from ..database import driver
from ..compilation_requete_fuzzy.reformulation_V3 import reformulate_fuzzy_query


search_routes = Blueprint("search", __name__)

@search_routes.route("/", methods=["GET"])
def search():
    query_text = request.args.get("query", "")
    # Le flag fuzzy (à envoyer depuis le frontend)
    fuzzy_flag = request.args.get("fuzzy", "false").lower() == "true"
    try:
        # Si la requête est fuzzy, on la reformule en requête crisp
        if fuzzy_flag:
            crisp_query = reformulate_fuzzy_query(query_text)
        else:
            crisp_query = query_text

        # Exécution de la requête sur Neo4j
        with driver.session() as session:
            result = session.run(crisp_query)
            results = [record.data() for record in result]
    except Exception as e:
        print(f"Erreur /search: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"results": results})

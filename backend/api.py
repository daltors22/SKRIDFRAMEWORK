from flask import Flask
from flask_cors import CORS
from flask import Flask, jsonify

from .database import close_db
from .routes.search import search_routes
from .routes.collections import collections_routes
from .routes.neo4j_queries import neo4j_routes
from .routes.scripts import script_routes
from .routes.files import files_routes
from flask import request

# ============================= Init Flask =============================#
app = Flask(__name__)
CORS(app)  # Autoriser les requêtes cross-origin (CORS)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Autorise toutes les requêtes CORS
app.config["DEBUG"] = True  # ✅ Active le mode débogage

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "403 Forbidden - Accès refusé"}), 403

# ✅ Accepter les requêtes JSON (très important)
@app.before_request
def before_request():
    if request.method in ["POST", "PUT", "GET"] and "application/json" in request.headers.get("Content-Type", ""):
        request.get_json(force=True, silent=True)

# ============================= Enregistrement des Routes =============================#
app.register_blueprint(search_routes, url_prefix="/search")
app.register_blueprint(collections_routes, url_prefix="/collections")
app.register_blueprint(neo4j_routes, url_prefix="/neo4j")
app.register_blueprint(script_routes, url_prefix="/scripts")
app.register_blueprint(files_routes, url_prefix="/files")
print(app.url_map)  # 🔥 Affiche toutes les routes de Flask

# ============================= Gestion propre de la BDD =============================#
@app.teardown_appcontext
def shutdown_session(exception=None):
    """ Ferme proprement la connexion à la BDD """
    close_db()

# ============================= Lancer l'API =============================#
if __name__ == '__main__':
    app.run(debug=True, port=5000)

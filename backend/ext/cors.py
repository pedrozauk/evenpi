from flask_cors import CORS

def init_app(app):
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
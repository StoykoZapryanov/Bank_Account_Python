from flask import Flask

def create_app():
    app = Flask(__name__)

    # Any additional setup or configuration goes here

    # Import and register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

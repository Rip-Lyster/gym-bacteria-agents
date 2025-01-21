from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from .core.config import get_config
from .routes import users, training_plans, exercise_types, workouts
from flask_talisman import Talisman
from flask_cors import CORS
import os
from datetime import datetime

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Initialize extensions
    from .core.models import init_db
    init_db(app)
    
    # Environment settings
    env = os.getenv('FLASK_ENV', 'development')
    is_development = env == 'development'
    
    # Enable CORS - more permissive for development
    CORS(app, 
         resources={r"/api/*": {
             "origins": ["http://localhost:3000"] if is_development else ["https://your-production-domain.com"],
             "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})
    
    # Security headers - more lenient in development
    Talisman(app,
        force_https=not is_development,
        strict_transport_security=not is_development,
        session_cookie_secure=not is_development,
        content_security_policy={
            'default-src': "'self'",
            'img-src': "'self' data: https:",
            'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
            'style-src': "'self' 'unsafe-inline'",
            'connect-src': "'self' https: http: *" if is_development else "'self' https:"
        }
    )
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    
    # Register blueprints
    app.register_blueprint(users.bp)
    app.register_blueprint(training_plans.bp)
    app.register_blueprint(exercise_types.bp)
    app.register_blueprint(workouts.bp)
    
    # Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Gym Bacteria API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return {"error": str(error.description)}, 400
        
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404
        
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500
    
    return app

app = create_app()

def run_app():
    """Run the application based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    host = os.getenv('FLASK_HOST', 'localhost')
    port = int(os.getenv('FLASK_PORT', 5328))
    
    if env == 'development':
        # Development mode - no SSL
        app.run(host=host, port=port, debug=True)
    else:
        # Production mode - with SSL
        cert_path = os.getenv('SSL_CERT_PATH', 'cert.pem')
        key_path = os.getenv('SSL_KEY_PATH', 'key.pem')
        app.run(host=host, port=port, ssl_context=(cert_path, key_path))

if __name__ == '__main__':
    run_app() 
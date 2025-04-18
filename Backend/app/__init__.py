from flask import Flask
from app.models.db import db
import os
from flask_cors import CORS
from flask_caching import Cache
import redis
from celery import Celery

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
cache = Cache(config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 300
})

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0",
        include=["app.celery_jobs.celery_tasks"]
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    print(os.getcwd())
    app = Flask(__name__)
    # Set CORS Policy
    
    CORS(app, resources={r"/*": {"origins": "http://localhost:4281"}})   
     
    # Set database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_prod.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "skndj#@IOD3oidnp1ow"
    
    app.config["CACHE_TYPE"] = "redis"
    app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0",
    
    cache.init_app(app)
    
    # Initialize the database
    db.init_app(app)
        
    #  DB is created if not present inside instance folder in root directory of run.py
    with app.app_context():
        db.create_all()
    
    # Initialize Celery
    celery = make_celery(app)
    app.extensions["celery"] = celery
    
    # Import and register routes from all controller files
    from app.controllers.authentication.auth_controller import authentication_routes
    from app.controllers.admin.admin_controller import admin_routes
    from app.controllers.service_professional.service_professional_controller import service_professional_routes
    from app.controllers.customer.customer_controller import customer_routes
    from app.controllers.service_info.service_info_controller import service_info_routes
    from app.controllers.request_info.request_info_controller import request_info_routes
    
    
    authentication_routes(app)
    admin_routes(app)
    service_professional_routes(app)
    customer_routes(app)
    service_info_routes(app)
    request_info_routes(app)
    
    return app, celery
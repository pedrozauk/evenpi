from dynaconf import FlaskDynaconf
from importlib import import_module

def load_extensions(app):
    for extensions in app.config.EXTENSIONS:
        module_name, factory = extensions.split(":")
        ext = import_module(module_name)
        getattr(ext,factory)(app)
        
def init_app(app):
    FlaskDynaconf(app)
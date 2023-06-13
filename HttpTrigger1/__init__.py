import logging
from backend.app import create_app
import azure.functions as func

app = create_app()

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)



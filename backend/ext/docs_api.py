from flasgger import Swagger


def init_app(app):
    swagger_config = Swagger.DEFAULT_CONFIG
    swagger_config['swagger'] = '2.0'
    swagger_config['openapi'] = '3.0.2'
    swagger_config['specs_route'] = '/swagger/'
    swagger_config['title'] = 'My API'
    swagger_config['description'] = 'My API Description'
    swagger_config['version'] = '0.0.1'
    swagger_config['uiversion'] = 3
    swagger_config['components'] = {'securitySchemes':{
                                                'acesstoken':{
                                                    'type':'http',
                                                    'scheme':'bearer',
                                                    'bearerFormat': 'JWT'},
                                                'refreshtoken':{
                                                    'type':'http',
                                                    'scheme':'bearer',
                                                    'bearerFormat': 'JWT'}

                                                    
                                            }}
    app.config['SWAGGER'] = swagger_config
    Swagger(app)

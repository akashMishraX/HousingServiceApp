from flask import Flask
from flask_bootstrap import Bootstrap4
from src.config import LocalDevelopmentConfig
from dotenv import load_dotenv
import os 
from src.routers._layout import BASE_URL


load_dotenv()
# importing models
from src.models.model import *

def init_app():
    app = Flask(__name__)
    bootstrap = Bootstrap4(app)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'cerulean'
    app.config.from_object(LocalDevelopmentConfig)
    app.app_context().push()
    db.init_app(app)
    return app
#exporting app
app = init_app()
# db.create_all()

#importing all routers
from src.routers.authRouter import *
from src.routers.homeRouter import *
from src.routers._role_create import *
from src.routers.customerRouter import *
from src.routers.professionalRouter import *
from src.routers._errorRouter import *
from src.routers.adminRouter import *


#listing server
if __name__ == "__main__":
    app.run(print(f'\n server is live on http://localhost:{os.getenv('PORT')}{BASE_URL} \n '),port=os.getenv('PORT'))

import os
from dotenv import load_dotenv
from distutils.util import strtobool

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def _get_list_var(var):
    out = []
    if var:
        out.extend(var.split(','))

    return out


class BaseConfig(object):
    # Secrets
    SECRET_KEY = os.getenv(
        'SECRET_KEY'
    ) or '<MMs8?u_;rTt>;LarIGI&FjWhKNSe=%3|W;=DFDqOdx+~-rBS+K=p8#t#9E+;{e$'

    ADMIN_EMAIL = os.getenv('DB_ADMIN_EMAIL') or 'admin@example.org'
    ADMIN_PASS = os.getenv('DB_ADMIN_PASSWORD') or 'admin'

    # Flask
    ERROR_INCLUDE_MESSAGE = False  # No default "message" field in error responses
    RESTX_MASK_SWAGGER = False  # No default MASK header in Swagger
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DB
    POSTGRES_HOST = os.getenv('POSTGRES_HOST') or 'localhost'
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', int())) or 5432
    POSTGRES_DB = os.getenv('POSTGRES_DB') or 'gis'
    POSTGRES_USER = os.getenv('POSTGRES_USER') or 'admin'
    POSTGRES_PASS = os.getenv('POSTGRES_PASS') or 'admin'
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL') or \
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    REDIS_HOST = os.getenv('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.getenv('REDIS_PORT', int())) or 6379
    REDIS_URL = f'redis://localhost:6379/0'

    # SMTP
    SMTP_HOST = os.getenv('SMTP_HOST') or 'localhost'
    SMTP_PORT = int(os.getenv('SMTP_PORT', int())) or 587
    SMTP_FROM = os.getenv('SMTP_FROM') or 'valhalla@kadas.org'
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASS = os.getenv('SMTP_PASS')
    SMTP_SECURE = bool(strtobool(os.getenv('SMTP_SECURE', 'True'))) or False  # evaluates to True

    # Dirs
    DATA_DIR = os.getenv('DATA_DIR') or os.path.join(basedir, 'data')
    TEMP_DIR = os.path.join(DATA_DIR, 'temp')

    # Input PBFs
    ENABLED_PROVIDERS = _get_list_var(os.getenv('ENABLED_PROVIDERS')) or ['osm']
    OSM_PBF_PATH = os.getenv('OSM_PBF_PATH') or os.path.join(DATA_DIR, 'planet-latest.osm.pbf')
    TOMTOM_PBF_PATH = os.getenv('TOMTOM_PBF_PATH') or os.path.join(DATA_DIR, 'planet-latest.tomtom.pbf')
    HERE_PBF_PATH = os.getenv('HERE_PBF_PATH') or os.path.join(DATA_DIR, 'planet-latest.tomtom.pbf')

    # Routers
    ENABLED_ROUTERS = _get_list_var(os.getenv('ENABLED_ROUTERS')) or ['valhalla']
    VALHALLA_IMAGE = os.getenv('VALHALLA_IMAGE') or 'gisops/valhalla:latest'
    OSRM_IMAGE = os.getenv('OSRM_IMAGE') or 'osrm/osrm-backend:latest'
    ORS_IMAGE = os.getenv('ORS_IMAGE') or 'openrouteservice/openrouteservice:latest'
    GRAPHHOPPER_IMAGE = os.getenv('GRAPHHOPPER_IMAGE') or 'graphhopper/graphhopper:latest'

    # create all dirs
    # temp is for intermediate files, i.e. graph etc
    # data is for persistent files, i.e. ZIP/TAR files
    for router in ENABLED_ROUTERS:
        os.makedirs(os.path.join(DATA_DIR, router), exist_ok=True)
        os.makedirs(os.path.join(TEMP_DIR, router), exist_ok=True)


class DevConfig(BaseConfig):
    REDIS_URL = f'redis://localhost:6379/0'


class ProdConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True

    POSTGRES_HOST = os.getenv('POSTGRES_HOST') or 'localhost'
    POSTGRES_PORT = os.getenv('POSTGRES_PORT') or '5432'
    POSTGRES_DB_TEST = 'gis_test'
    POSTGRES_USER = os.getenv('POSTGRES_USER') or 'admin'
    POSTGRES_PASS = os.getenv('POSTGRES_PASS') or 'admin'

    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_TEST_URL') or \
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}'

    OSM_PBF_PATH = os.path.join(basedir, 'tests', 'data', 'andorra-200827.osm.pbf')
    TOMTOM_PBF_PATH = os.path.join(basedir, 'tests', 'data', 'liechtenstein-201109.tomtom.pbf')

    ADMIN_EMAIL = 'admin@example.org'
    ADMIN_PASS = 'admin'

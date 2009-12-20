from repoze.bfg.configuration import Configurator

from tutorial.models import DBSession
from tutorial.models import initialize_sql
from tutorial.models import RootFactory

class Cleanup:
    def __init__(self, cleaner):
        self.cleaner = cleaner
    def __del__(self):
        self.cleaner()

def handle_teardown(event):
    environ = event.request.environ
    environ['tutorial.sasession'] = Cleanup(DBSession.remove)

def app(global_config, **settings):
    """ This function returns a repoze.bfg.router.Router object.
    
    It is usually called by the PasteDeploy framework during ``paster serve``.
    """
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    initialize_sql(db_string)
    config = Configurator(settings=settings, root_factory=RootFactory)
    config.begin()
    config.load_zcml('configure.zcml')
    config.end()
    return config.make_wsgi_app()

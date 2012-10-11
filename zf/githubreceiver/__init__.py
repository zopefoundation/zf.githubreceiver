from pyramid.config import Configurator


class Root(object):
    def __init__(self, request):
            self.request = request

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.include('pyramid_mailer')
    config.include('pyramid_tm')
    config.include('githubevent')
    config.scan('.subscriber')
    return config.make_wsgi_app()

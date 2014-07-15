from flask import current_app
from flask import _app_ctx_stack as stack

class ActorFlask(object):

  def __init__(self, polar_client, actor_name, app=None):
    self.app = app

    if app is not None:
      self.init_app(app)

  def init_app(self, app):
    app.teardown_appcontext(self.teardown)

  def teardown(self, exception):
    pass

  @property
  def system(self):
    pass

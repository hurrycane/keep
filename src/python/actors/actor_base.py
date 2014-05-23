class Actor(object):

  @classmethod
  def props(cls, **kwargs):
    return cls(**kwargs)

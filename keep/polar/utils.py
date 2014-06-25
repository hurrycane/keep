from time import sleep

class retry(object):

  def __init__(self, exception, times, backoff):
    self.exception = exception
    self.times = times
    self.backoff = backoff

  def __call__(self, func):
    def wrapped_func(*args, **kwargs):
      for i in range(self.times - 1):
        try:
          return func(*args, **kwargs)
        except self.exception:
          sleep(self.backoff ** (i+1))

      return func(*args, **kwargs)

    return wrapped_func

import math

from .exceptions import NotEnoughData

MATH_EXP_MAX = 709

class AccuralFailureDetector(object):

  def __init__(self, history):
    if len(history) < 10:
      raise NotEnoughData("Heartbeat history needs to contain at least two value")

    self.heartbeat_history = []

    history = list(history)[::-1]
    last_element = history[0]

    for item in history[1:]:
      self.heartbeat_history.append(last_element - item)
      last_element = item

    self.mean = self._mean(self.heartbeat_history)

  def _mean(self, arr):
    return sum(arr) * 1.0 / len(arr)

  def phi(self, t):
    """
    phi = -log10(1 - F(timeSinceLastHeartbeat))

    F is the CDF of the event distribution. For the exponential distribution,
    the CDF is: 1 - e^(-Lt) and L is given by 1/mean

    F(t) = 1 - (1 - e^(-t/mean))

    phi = -log10(1 - (1 - e^(-t/mean)))
    phi = -log10(e^(-t/mean)) = -log(e^(-t/mean)) / log(10) = (t/mean) / log(10)
        = t/mean * 1/ln(10) = t/mean * 0.4342945
    """
    return t / self.mean * 0.4342945

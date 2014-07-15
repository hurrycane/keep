import math

from .exceptions import NotEnoughData

MATH_EXP_MAX = 709

class AccuralFailureDetector(object):

  def __init__(self, history):
    if len(history) < 3:
      raise NotEnoughData("Heartbeat history needs to contain at least two value")

    self.heartbeat_history = []

    history = list(history)[::-1]
    last_element = history[0]

    for item in history[1:]:
      self.heartbeat_history.append(last_element - item)
      last_element = item

    self.mean = self._mean(self.heartbeat_history)

  def _mean(self, arr):
    return sum(arr) / float(len(arr))

  def _stdv(self, arr):
    mean = self._mean(arr)
    # TODO std lol
    std = 0

    for elem in arr:
      std = std + (elem - mean)**2

    std = math.sqrt(std / float(len(arr)-1))
    return std

  def phi(self, t):
    """
    phi = -log10(1 - F(timeSinceLastHeartbeat))

    -log10(1 - (1/2 * (1 + math.erf((timeSinceLastHeartbeat - mean)/(stdev * sqrt(2)))))

    F is the CDF of the event distribution. For the exponential distribution,
    the CDF is: 1 - e^(-Lt) and L is given by 1/mean

    F(t) = 1 - (1 - e^(-t/mean))

    phi = -log10(1 - (1 - e^(-t/mean)))
    phi = -log10(e^(-t/mean)) = -log(e^(-t/mean)) / log(10) = (t/mean) / log(10)
        = t/mean * 1/ln(10) = t/mean * 0.4342945
    """

    return float(t) / float(self._mean(self.heartbeat_history)) * 0.4342945

from keep.crow.phi_accrual_failure_detector import AccuralFailureDetector

history = [
  1404557650.660614,
  1404557651.303978,
  1404557651.956007,
  1404557652.602867,
  1404557653.495276,
  1404557654.064848,
  1404557654.633967,
  1404557655.222162,
  1404557655.869532,
  1404557656.764198,
  1404557657.361267,
  1404557657.972642,
  1404557658.539059,
  1404557659.150412,
  1404557659.798591,
  1404557660.44681,
  1404557661.099742,
  1404557661.993596,
  1404557662.562113,
  1404557663.150115,
  1404557663.718242
]

def xfrange(start, stop, step):
  while start < stop:
    yield start
    start += step

def test_infinity():
  failure_detector = AccuralFailureDetector(history)
  #assert failure_detector.phi(4) == float("inf")

def test_initial_accural():
  for i in range(10,len(history)):
    failure_detector = AccuralFailureDetector(history[0:i])
    for t in xfrange(0, 20, 0.1):
      t, failure_detector.phi(t)

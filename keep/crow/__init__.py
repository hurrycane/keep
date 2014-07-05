import logging
import sys

def set_up_logging(name):
  log = logging.getLogger(name)
  out_hdlr = logging.StreamHandler(sys.stdout)
  out_hdlr.setFormatter(logging.Formatter("[%(asctime)s %(filename)s:%(lineno)s - %(funcName)s] %(message)s"))
  out_hdlr.setLevel(logging.DEBUG)
  log.addHandler(out_hdlr)
  log.setLevel(logging.DEBUG)

from .crow_context import CrowContext

"""
Address Service
"""
# Python
from abc import ABCMeta
from abc import abstractmethod
from collections import namedtuple
import logging
# * * *
from .provider_base import ProviderBase

log = logging.getLogger(__name__)

class Normalizer(ProviderBase, metaclass=ABCMeta):
  # Registered providers get added to this dict
  providers = {}

  NormalizeResult = namedtuple("NormalizeResult", [
    "success",          # bool: True if the lookup was successful
    "line1",
    "line2",
    "city",
    "state",
    "postalCode",
    "raw",
  ])
  NORMALIZE_FAILED = NormalizeResult(success=False, line1=None, line2=None, city=None, state=None, postalCode=None, raw=None)
  
  @abstractmethod
  def normalize(self, line1, line2, city, state, postalCode):
    """
    Normalize the address

    Args:
      line1 (str): street number and name
      line2 (str): suite, apartment, etc.
      city (str): city
      state (str): state
      postalCode (str): postal code

    Returns:
      NormalizeResult
    """
    raise NotImplementedError("Implement this method in the child class")

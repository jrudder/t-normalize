"""
Local Normalizer
"""
# Python
import logging
# * * *
from .normalizer import Normalizer

log = logging.getLogger(__name__)

@Normalizer.register(name="local")
class NormalLocal(Normalizer):
  STREET_TYPES = {
    "pl"     : "Pl",
    "place"  : "Pl",
    "st"     : "St",
    "street" : "St",
    "ave"    : "Ave",
    "avenue" : "Ave",
  }
  
  def __init__(self, config):
    pass

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
      LookupResult
    """

    ##########
    # Lines
    
    # Tokenize and check the last value for street type indicators
    lines_split = line1.split(" ")
    for k in self.__class__.STREET_TYPES.keys():
      if lines_split[-1].lower()==k:
        lines_split[-1] = self.__class__.STREET_TYPES[k]
        line1 = " ".join(lines_split)
        break

    return Normalizer.NormalizeResult(
      success    = True,
      line1      = line1,
      line2      = line2,
      city       = city,
      state      = state,
      postalCode = postalCode,
      raw        = None)

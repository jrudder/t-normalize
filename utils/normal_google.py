"""
Google Normalizer
"""
# Python
import logging
# 3rd Party
import pygeocoder
# * * *
from .normalizer import Normalizer

log = logging.getLogger(__name__)

@Normalizer.register(name="google")
class NormalGoogle(Normalizer):
  
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

    if line2 is not None:
      lines = "{} {}".format(line1, line2)
    else:
      lines = line1
      
    g = pygeocoder.Geocoder().geocode("{} {} {} {} {}".format(
      lines, city, state, "US", postalCode))
    parsed = {e["types"][0]: e["short_name"] for e in g.data[0]["address_components"]}

    try:
      result = Normalizer.NormalizeResult(
        success    = True,
        line1      = "{} {}".format(parsed["street_number"], parsed["route"]),
        line2      = None,
        city       = parsed["locality"],
        state      = parsed["administrative_area_level_1"],
        postalCode = parsed["postal_code"],
        raw        = g.data)
    except:
      result = Normalizer.NormalizeResult(
        success    = True,
        line1      = None,
        line2      = None,
        city       = None,
        state      = None,
        postalCode = None,
        raw        = g.data)

    return result
"""
Texas A&M Geoservices Normalizer
"""
# Python
import logging
# 3rd Party
import pygeocoder
import requests
import simplejson as json
# * * *
from .normalizer import Normalizer

log = logging.getLogger(__name__)

@Normalizer.register(name="here")
class NormalHere(Normalizer):
  def __init__(self, config):
    self.uri = "https://geocoder.cit.api.here.com/6.2/geocode.json"
    self.query_base = {
      "app_id": config["app_id"],
      "app_code": config["app_code"],
      "gen": "8",
    }

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

    if line2 is None:
      lines = line1
    else:
      lines = "{} {}".format(line1, line2)
      
    query = self.query_base.copy()
    query["searchtext"] = "{} {} {} {}".format(
      lines, city, state, postalCode)

    response = requests.get(self.uri, params=query)

    if response.status_code != 200:
      log.error("Failed to send request: {}\n{}".format(response.status_code, response.text))
      result = Normalizer.NORMALIZE_FAILED
    else:
      try:
        raw_text = json.dumps(json.loads(response.text), indent=4)
      except:
        raw_text = response.text
      result = self.__class__._parse(raw_text)

    return result

  @classmethod
  def _parse(cls, text):
    """ Parse the json text into a Normalizer.NormalizeResult """
    
    try:
      data = json.loads(text)["Response"]["View"][0]["Result"][0]["Location"]["Address"]
      result = Normalizer.NormalizeResult(
          success    = True,
          line1      = "{} {}".format(data["HouseNumber"], data["Street"]) if "HouseNumber" in data and "Street" in data else None,
          line2      = None,
          city       = data.get("City", None),
          state      = data.get("State", None),
          postalCode = data.get("PostalCode", None),
          raw        = text)
    except:
      log.error("Failed to parse", exc_info=True)
      result = Normalizer.NormalizeResult(
          success    = True,
          line1      = None,
          line2      = None,
          city       = None,
          state      = None,
          postalCode = None,
          raw        = text)

    return result

  @classmethod
  def _get_or_none(cls, node, path):
    """ Get the text of the element of node at path or None """
    element = node.find(path)
    if element is not None:
      result = element.text
    else:
      result = None

    return result
    
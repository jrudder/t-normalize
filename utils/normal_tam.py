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

@Normalizer.register(name="tam")
class NormalTam(Normalizer):
  
  def __init__(self, config):
    self.uri = "https://geoservices.tamu.edu/Services/AddressNormalization/WebService/v04_01/Rest/"
    self.query_base = {
      "apikey": config["apikey"],
      "responseFormat": "json",
      "notStore": "false",
      "version": "4.01",
      "addressFormat": "USPSPublication28",
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
    query["nonParsedStreetAddress"] = lines
    query["nonParsedCity"] = city
    query["nonParsedState"] = state
    query["nonParsedZip"] = postalCode

    response = requests.get(self.uri, data=query)

    if response.status_code != 200:
      log.error("Failed to send request: {}\n{}".format(response.status_code, response.text))
      result = Normalizer.NORMALIZE_FAILED
    else:
      result = self.__class__._parse(response.text)

    return result

  @classmethod
  def _parse(cls, text):
    """ Parse the json text into a Normalizer.NormalizeResult """
    
    try:
      data = json.loads(text)["StreetAddresses"][0]
      result = Normalizer.NormalizeResult(
          success    = True,
          line1      = "{} {}".format(data["Number"], data["StreetName"]),
          line2      = "{} {}".format(data["SuiteType"], data["SuiteNumber"]) if len(data["SuiteType"])>0 else None,
          city       = data.get("City", None),
          state      = data.get("State", None),
          postalCode = data.get("ZIP", None),
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
    
"""
Yahoo Normalizer
"""
# Python
import logging
import urllib.parse
# 3rd Party
import pygeocoder
import requests
from requests_oauthlib import OAuth1
import oauthlib
import simplejson as json
# * * *
from .normalizer import Normalizer

log = logging.getLogger(__name__)

@Normalizer.register(name="yahoo")
class NormalYahoo(Normalizer):
  def __init__(self, config):
    self.uri = "http://yboss.yahooapis.com/geo/placefinder?flags=J&location={}"
    self.key    = config["CONSUMER_KEY"]
    self.secret = config["CONSUMER_SECRET"]

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
    
    # Query string param
    location = urllib.parse.quote("{} {} {} {}".format(lines, city, state, postalCode))

    # OAuth signing
    client = oauthlib.oauth1.Client(self.key,
        client_secret=self.secret,
        signature_type=oauthlib.oauth1.SIGNATURE_TYPE_AUTH_HEADER)
    uri, headers, body = client.sign(self.uri.format(location))

    # Send request
    response = requests.get(uri, headers=headers)

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
      data = json.loads(text)["bossresponse"]["placefinder"]["results"][0]
      result = Normalizer.NormalizeResult(
          success    = True,
          line1      = data.get("line1", None),
          line2      = None,
          city       = data.get("city", None),
          state      = data.get("state", None),
          postalCode = data.get("uzip", None),
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
    
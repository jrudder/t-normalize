"""
USPS Normalizer
"""
# Python
import logging
# 3rd Party
from defusedxml import ElementTree
import pygeocoder
import requests
# * * *
from .normalizer import Normalizer

log = logging.getLogger(__name__)

@Normalizer.register(name="usps")
class NormalUsps(Normalizer):
  
  def __init__(self, config):
    self.uri = "https://secure.shippingapis.com/ShippingAPI.dll?API=Verify&XML="
    self.username = config["username"]
    self.password = config["password"]

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

    xml = ("""<AddressValidateRequest USERID="{username}">""" +
          """<IncludeOptionalElements>false</IncludeOptionalElements>""" +
          """<ReturnCarrierRoute>false</ReturnCarrierRoute>""" +
          """<Address ID="0">""" +
          """<FirmName/>""" +
          """<Address1>{line2}</Address1>""" +
          """<Address2>{line1}</Address2>""" +
          """<City>{city}</City>""" +
          """<State>{state}</State>""" +
          """<Zip5>{zip5}</Zip5>""" +
          """<Zip4>{zip4}</Zip4>""" +
          """</Address>""" +
          """</AddressValidateRequest>""")
    xml = xml.format(
      username = self.username,
      line1 = line1 if line1 is not None else "",
      line2 = line2 if line2 is not None else "",
      city = city,
      state = state,
      zip5 = postalCode[:5]  if postalCode is not None else "",
      zip4 = postalCode[-4:] if postalCode is not None and len(postalCode) > 5 else "")
    
    print(xml)

    response = requests.get(self.uri + xml)
    if response.status_code != 200:
      log.error("Failed to send request: {}\n{}".format(response.status_code, response.text))
      result = Normalizer.NORMALIZE_FAILED
    else:
      result = self.__class__._parse(response.text)

    return result

  @classmethod
  def _parse(cls, xml):
    """ Parse the XML into a Normalizer.NormalizeResult """
    try:
      node = ElementTree.fromstring(xml).find("Address")
    except ElementTree.ParseError:
      log.error("Failed to parse xml", exc_info=True)
      return NormalFactory.NORMALIZE_FAILED

    try:
      result = Normalizer.NormalizeResult(
          success    = True,
          line1      = cls._get_or_none(node, "Address2"),
          line2      = cls._get_or_none(node, "Address1"),
          city       = cls._get_or_none(node, "City"),
          state      = cls._get_or_none(node, "State"),
          postalCode = cls._get_or_none(node, "Zip5"),
          raw        = xml)
    except:
      log.error("Failed to parse", exc_info=True)
      result = Normalizer.NormalizeResult(
          success    = True,
          line1      = None,
          line2      = None,
          city       = None,
          state      = None,
          postalCode = None,
          raw        = xml)

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
    
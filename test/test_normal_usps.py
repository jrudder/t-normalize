# * * *
from utils.normal_usps import NormalUsps

def test_parse_ok():
  """ Test parsing a good response """
  xml = """<AddressValidateResponse>
    <Address ID="0">
      <Address2>205 BAGWELL AVE</Address2>
      <City>NUTTER FORT</City>
      <State>WV</State>
      <Zip5>26301</Zip5>
      <Zip4>4322</Zip4>
      <DeliveryPoint>05</DeliveryPoint>
      <CarrierRoute>C025</CarrierRoute>
    </Address>
  </AddressValidateResponse>"""

  result = NormalUsps._parse(xml)
  assert result.raw == xml
  assert result.line1 == "205 BAGWELL AVE"
  assert result.line2 == None
  assert result.city  == "NUTTER FORT"
  assert result.state == "WV"
  assert result.postalCode == "26301"

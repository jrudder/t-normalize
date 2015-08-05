# * * *
from utils.normal_tam import NormalTam

def test_parse_ok():
  """ Test parsing a good response """
  text = """{
    "TransactionId" : "ffeb9d2e-1428-4c8a-b8fb-21b1d8141735",
    "Version"   : "4.01",
    "QueryStatusCode" : "Success",
    "StreetAddresses" : 
    [
      {
      "Number" : "123",
      "NumberFractional" : "",
      "PreDirectional" : "",
      "PreQualifier" : "",
      "PreType" : "",
      "PreArticle" : "",
      "StreetName" : "OLD US 25",
      "Suffix" : "",
      "PostArticle" : "",
      "PostQualifier" : "",
      "PostDirectional" : "",
      "SuiteType" : "",
      "SuiteNumber" : "",
      "City" : "LOS ANGELES",
      "State" : "CA",
      "ZIP" : "90089",
      "ZIPPlus1" : "",
      "ZIPPlus2" : "",
      "ZIPPlus3" : "",
      "ZIPPlus4" : "0255",
      "ZIPPlus5" : "",
      "PostOfficeBoxType" : "",
      "PostOfficeBoxNumber" : ""
      }
    ]
  }
  """

  result = NormalTam._parse(text)
  assert result.raw == text
  assert result.line1 == "123 OLD US 25"
  assert result.line2 == None
  assert result.city  == "LOS ANGELES"
  assert result.state == "CA"
  assert result.postalCode == "90089"

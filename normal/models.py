# Python
import hashlib
# Django
from django.db import models

class Address(models.Model):
  """
  Represents a single address input
  """
  id    = models.CharField(max_length=64, primary_key=True)
  lines = models.CharField(max_length=200)
  city  = models.CharField(max_length=64)
  state = models.CharField(max_length=2)
  postalCode = models.CharField(max_length=5)

  normal = models.ForeignKey("AddressNormal")

  def __str__(self):
    return "|".join([s for s in (self.lines, self.city, self.state, self.postalCode) if s is not None and len(s)!=0])

  def get_hash(self):
    return hashlib.new("sha256", str(self).encode()).hexdigest()
  def set_hash(self):
    self.id = self.get_hash()

  class Meta:
    verbose_name_plural = "Addresses"

class AddressNormal(models.Model):
  # Hash of the normalized address
  id    = models.CharField(max_length=64, primary_key=True)

  # Normalized Address
  lines = models.CharField(max_length=200)
  city  = models.CharField(max_length=64)
  state = models.CharField(max_length=2)
  postalCode = models.CharField(max_length=5)

  @classmethod
  def get_or_create_normal(cls, **kwargs):
    addr = Address(**kwargs)
    addr_hash = hashlib.new(
      "sha256",
      str(addr).encode()).hexdigest()

    obj, created = AddressNormal.objects.get_or_create(id=addr_hash, **kwargs)
    return obj, created

  def __str__(self):
    return self.id

class Lookup(models.Model):
  provider = models.CharField(max_length=32, null=True, blank=True)

  in_line1 = models.CharField(max_length=255, null=True, blank=True)
  in_line2 = models.CharField(max_length=255, null=True, blank=True)
  in_city  = models.CharField(max_length=255, null=True, blank=True)
  in_state = models.CharField(max_length=255, null=True, blank=True)
  in_postalCode = models.CharField(max_length=10, null=True, blank=True)
  in_country = models.CharField(max_length=255, null=True, blank=True)

  out_line1 = models.CharField(max_length=255, null=True, blank=True)
  out_line2 = models.CharField(max_length=255, null=True, blank=True)
  out_city  = models.CharField(max_length=255, null=True, blank=True)
  out_state = models.CharField(max_length=255, null=True, blank=True)
  out_postalCode = models.CharField(max_length=10, null=True, blank=True)
  out_country = models.CharField(max_length=255, null=True, blank=True)
  out_raw = models.TextField(null=True, blank=True)

  @property
  def in_dict(self):
    """ dict of the lookup input """
    return {
      "lines": self.in_lines,
      "city": self.in_city,
      "state": self.in_state,
      "postalCode": self.in_postalCode,
      "country": self.in_country}

  @property
  def out_dict(self):
    """ dict of the lookup output """
    return {
      "provider": self.provider,
      "line1": self.out_line1,
      "line2": self.out_line2,
      "city": self.out_city,
      "state": self.out_state,
      "postalCode": self.out_postalCode,
      "country": self.out_country}

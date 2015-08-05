# Django
from django.shortcuts import render
from django.template import Context
from django.core.paginator import Paginator
from django.conf import settings
# * * *
from normal.models import Address
from normal.models import AddressNormal
from normal.models import Lookup
from utils.normalizer import Normalizer
from utils.normal_local   import NormalLocal
from utils.normal_google  import NormalGoogle
from utils.normal_usps    import NormalUsps
from utils.normal_tam     import NormalTam

def normalize(request):
  """
  Normalize the address
  """

  # Pull form fields
  lines      = request.POST.get("lines",      "")
  city       = request.POST.get("city",       "")
  state      = request.POST.get("state",      "")
  postalCode = request.POST.get("postalCode", "")
  page       = request.GET.get("page", 1)

  # Create context
  ctx = {
    "input": {
      "lines"      : lines,
      "city"       : city,
      "state"      : state,
      "postalCode" : postalCode},
    "normals": [],
    "history": None,
  }

  if request.method == "POST":
    # Get the normalizers
    normalizers = [
      #Normalizer.get("local"),
      Normalizer.get("google"),
      Normalizer.get("usps", config=settings.PROVIDERS["usps"]),
      Normalizer.get("tam", config=settings.PROVIDERS["tam"]),
    ]

    for normalizer in normalizers:
      # Normalize
      result = normalizer.normalize(
        line1 = lines,
        line2 = None,
        city  = city,
        state = state,
        postalCode = postalCode)

      # Record the result
      lookup = Lookup.objects.create(
        provider = normalizer.name,
        in_line1 = lines,
        in_line2 = None,
        in_city  = city,
        in_state = state,
        in_postalCode = postalCode,
        out_line1 = result.line1,
        out_line2 = result.line2,
        out_city  = result.city,
        out_state = result.state,
        out_postalCode = result.postalCode,
        out_raw = result.raw)

      # Add to context
      ctx["normals"].append(lookup.out_dict)

  # Add history
  history = Paginator(Lookup.objects.all().order_by("-pk"), 20)
  ctx["history"] = history.page(page)

  return render(request, "normalize.html", ctx)

def x_normalize(request):
  """
  Normalize the address
  """

  # Pull form fields
  lines      = request.POST.get("lines",      "")
  city       = request.POST.get("city",       "")
  state      = request.POST.get("state",      "")
  postalCode = request.POST.get("postalCode", "")

  # Normalize
  n_dict = norm(lines, city, state, postalCode)

  # Set context
  ctx = {
    "input": {
      "lines"      : lines,
      "city"       : city,
      "state"      : state,
      "postalCode" : postalCode},
    "normal": n_dict,
    "normal_found": None,
  }  

  # Get or create the normal
  n_obj, ctx["normal_found"] = AddressNormal.get_or_create_normal(**n_dict)

  # Create the address (if needed)
  input_obj = Address(**ctx["input"])
  input_obj.set_hash()
  input_obj.normal = n_obj
  if Address.objects.filter(id=input_obj.get_hash()).count()==0:
    ctx["saved"] = True
    input_obj.save()
  else:
    ctx["saved"] = False

  return render(request, "normalize.html", ctx)

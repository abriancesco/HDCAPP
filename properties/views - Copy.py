from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse
import pdfkit
from .models import Property


# ============================================================
# PROPERTY SEARCH VIEW
# ============================================================
def property_search(request):
    qs = Property.objects.all()

    selected_ids = set(request.GET.getlist("selected_ids"))
    newly_checked = request.GET.getlist("selected_ids")
    selected_ids.update(newly_checked)

    try:
        selected_ids = list(map(int, selected_ids))
    except ValueError:
        selected_ids = []

    request.session["selected_comps"] = selected_ids
    request.session.modified = True

    show_selected_only = request.GET.get("show_selected_only")

    if show_selected_only:
        selected_ids = request.session.get("selected_comps", [])
        qs = Property.objects.filter(id__in=selected_ids)

        request.GET = request.GET.copy()
        for key in [
            "size_min", "size_max",
            "price_min", "price_max",
            "date_start", "date_end",
            "location", "access", "county",
            "sort", "page"
        ]:
            if key in request.GET:
                del request.GET[key]

    if request.GET.get("clear_all"):
        selected_ids = []
        request.session["selected_comps"] = []
        request.session.modified = True

        request.GET = request.GET.copy()
        for key in [
            "size_min", "size_max",
            "price_min", "price_max",
            "date_start", "date_end",
            "location", "access", "county",
            "sort", "page"
        ]:
            if key in request.GET:
                del request.GET[key]

    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    size_min = to_float(request.GET.get("size_min"))
    size_max = to_float(request.GET.get("size_max"))
    price_min = to_float(request.GET.get("price_min"))
    price_max = to_float(request.GET.get("price_max"))

    if size_min is not None:
        qs = qs.filter(site_size__gte=size_min)
    if size_max is not None:
        qs = qs.filter(site_size__lte=size_max)
    if price_min is not None:
        qs = qs.filter(sale_price__gte=price_min)
    if price_max is not None:
        qs = qs.filter(sale_price__lte=price_max)

    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    if date_start:
        qs = qs.filter(sale_date__gte=date_start)
    if date_end:
        qs = qs.filter(sale_date__lte=date_end)

    location = request.GET.get("location")
    access = request.GET.get("access")
    county = request.GET.get("county")

    if location:
        qs = qs.filter(address__icontains=location)
    if access:
        qs = qs.filter(access__icontains=access)
    if county:
        qs = qs.filter(county__icontains=county)

    sort = request.GET.get("sort", "sale_date")
    allowed_sorts = [
        "sale_price", "-sale_price",
        "sale_date", "-sale_date",
        "site_size", "-site_size",
        "address", "-address",
    ]
    if sort in allowed_sorts:
        qs = qs.order_by(sort)

    paginator = Paginator(qs, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "sort": sort,
        "total_results": qs.count(),
        "selected_ids": selected_ids,
        "request": request,
    }

    return render(request, "properties/search.html", context)


# ============================================================
# COMP LIST VIEW
# ============================================================
def comp_list(request):
    selected = request.session.get("selected_comps", [])
    comps = Property.objects.filter(id__in=selected)

    return render(request, "properties/comp_list.html", {
        "comps": comps,
        "selected": selected,
    })


# ============================================================
# COMP EDIT VIEW
# ============================================================
def comp_edit(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if "comp_forms" not in request.session:
        request.session["comp_forms"] = {}

    comp_forms = request.session["comp_forms"]
    selected = request.session.get("selected_comps", [])

    pid = str(property_id)

    if pid not in comp_forms:
        comp_forms[pid] = {
            'comp_number': selected.index(property_id) + 1 if property_id in selected else 1,
            'location': property_obj.address or "",
            'county': property_obj.county or "",
            'access': property_obj.access or "",
            'size': float(property_obj.site_size) if property_obj.site_size is not None else "",
            'sqft': float(property_obj.sqft) if property_obj.sqft is not None else "",
            'utilities': "",
            'water': "",
            'improvements': "",
            'eco': "",
            'terrain': "",
            'restrictions': "",
            'price': float(property_obj.sale_price) if property_obj.sale_price is not None else "",
            'sale_date': property_obj.sale_date.strftime('%Y-%m-%d') if property_obj.sale_date else "",
            'price_per_acre': "",
            'grantor': "",
            'grantee': "",
            'document_no': "",
            'terms': "",
            'listing': "",
            'broker': "",
            'verified_to': "",
            'verified_by': "",
            'verified_date': "",
            'inspected_by': "",
            'inspected_date': "",
            'appraiser_name': "",
            'comments': property_obj.comments or "",
        }

    if request.method == 'POST':
        for key in comp_forms[pid].keys():
            if key in request.POST:
                comp_forms[pid][key] = request.POST[key]

        try:
            price = float(comp_forms[pid]['price'])
            size = float(comp_forms[pid]['size'])
            if size > 0:
                comp_forms[pid]['price_per_acre'] = round(price / size, 2)
        except:
            comp_forms[pid]['price_per_acre'] = ""

        request.session["comp_forms"] = comp_forms
        request.session.modified = True

    prev_id = next_id = None

    if property_id in selected:
        idx = selected.index(property_id)
        if idx > 0:
            prev_id = selected[idx - 1]
        if idx < len(selected) - 1:
            next_id = selected[idx + 1]

    return render(request, "properties/comp_edit.html", {
        'comp': comp_forms[pid],
        'property': property_obj,
        'prev_id': prev_id,
        'next_id': next_id,
        'selected_ids': selected,
        'total_comps': len(selected),
        'comp_number': comp_forms[pid]['comp_number'],
    })


# ============================================================
# PDF VIEW
# ============================================================
def comp_pdf(request, property_id):
    comp_forms = request.session.get("comp_forms", {})
    pid = str(property_id)

    if pid not in comp_forms:
        return HttpResponse("No working copy found for this comp.")

    comp = comp_forms[pid]
    property_obj = Property.objects.get(id=property_id)

    html = render_to_string("properties/comp_pdf.html", {
        "comp": comp,
        "property": property_obj,
    })

    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=comp_{property_id}.pdf"

    return response


# ============================================================
# PREVIEW ALL COMPS
# ============================================================
def comp_preview(request):
    selected = request.session.get("selected_comps", [])
    comp_forms = request.session.get("comp_forms", {})

    comps = []
    for cid in selected:
        pid = str(cid)
        if pid in comp_forms:
            comps.append({
                "property": Property.objects.get(id=cid),
                "form": comp_forms[pid],
            })

    return render(request, "properties/comp_preview.html", {
        "comps": comps,
    })


# ============================================================
# START EDITING — GO DIRECTLY TO FIRST SELECTED COMP
# ============================================================
def comp_start(request):
    selected = request.session.get("selected_comps", [])

    if not selected:
        return redirect("/")

    first_id = selected[0]
    return redirect(f"/comp/{first_id}/")

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse
import pdfkit
from .forms import PropertyForm, PropertyImageFormSet
from .models import Property, PropertyImage


# ============================================================
# PROPERTY SEARCH VIEW
# ============================================================
def property_search(request):
    qs = Property.objects.filter(deleted=False)

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
        qs = qs.filter(size__gte=size_min)
    if size_max is not None:
        qs = qs.filter(size__lte=size_max)

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
        qs = qs.filter(location__icontains=location)
    if access:
        qs = qs.filter(access__icontains=access)
    if county:
        qs = qs.filter(county__icontains=county)

    sort = request.GET.get("sort", "sale_date")
    allowed_sorts = [
        "sale_price", "-sale_price",
        "sale_date", "-sale_date",
        "size", "-size",
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
    comps = Property.objects.filter(id__in=selected, deleted=False)

    return render(request, "properties/comp_list.html", {
        "comps": comps,
        "selected": selected,
    })


# ============================================================
# COMP EDIT VIEW
# ============================================================
def comp_edit(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id, deleted=False)

    if "comp_forms" not in request.session:
        request.session["comp_forms"] = {}

    comp_forms = request.session["comp_forms"]
    selected = request.session.get("selected_comps", [])

    pid = str(property_id)

    if pid not in comp_forms:
        comp_forms[pid] = {
            'comp_number': selected.index(property_id) + 1 if property_id in selected else 1,
            'location': property_obj.location or "",
            'county': property_obj.county or "",
            'access': property_obj.access or "",
            'size': float(property_obj.size) if property_obj.size is not None else "",
            'sqft': float(property_obj.sqft) if property_obj.sqft is not None else "",
            'utilities': property_obj.utilities or "",
            'water': property_obj.water or "",
            'improvements': property_obj.improvements or "",
            'eco': property_obj.eco or "",
            'terrain': property_obj.terrain or "",
            'restrictions': property_obj.restrictions or "",
            'price': float(property_obj.sale_price) if property_obj.sale_price is not None else "",
            'sale_date': property_obj.sale_date.strftime('%Y-%m-%d') if property_obj.sale_date else "",
            'price_per_acre': "",
            'grantor': property_obj.grantor or "",
            'grantee': property_obj.grantee or "",
            'document_no': property_obj.bk_pg or "",
            'terms': property_obj.terms or "",
            'listing': property_obj.listing or "",
            'broker': property_obj.broker or "",
            'verified_to': property_obj.verified_to or "",
            'verified_by': property_obj.verified_by or "",
            'verified_date': property_obj.verified_date.strftime('%Y-%m-%d') if property_obj.verified_date else "",
            'inspected_by': property_obj.inspected_by or "",
            'inspected_date': property_obj.inspected_date.strftime('%Y-%m-%d') if property_obj.inspected_date else "",
            'appraiser_name': property_obj.appraiser_name or "",
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
# PDF VIEW (ONE COMP)
# ============================================================
def comp_pdf(request, property_id):
    comp_forms = request.session.get("comp_forms", {})
    pid = str(property_id)

    if pid not in comp_forms:
        return HttpResponse("No working copy found for this comp.")

    comp = comp_forms[pid]
    property_obj = Property.objects.get(id=property_id, deleted=False)

    images = PropertyImage.objects.filter(property=property_obj)

    for img in images:
        img.fixed_path = img.image.path.replace("\\", "/")

    html = render_to_string("properties/comp_pdf.html", {
        "comp": comp,
        "property": property_obj,
        "images": images,
    })

    options = {"enable-local-file-access": True}

    pdf = pdfkit.from_string(html, False, options=options)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=comp_{property_id}.pdf"

    return response


# ============================================================
# PDF VIEW (ALL COMPS)
# ============================================================
def comp_pdf_all(request):
    selected = request.session.get("selected_comps", [])
    comp_forms = request.session.get("comp_forms", {})

    comps = []
    for cid in selected:
        pid = str(cid)
        if pid in comp_forms:
            property_obj = Property.objects.get(id=cid, deleted=False)
            images = PropertyImage.objects.filter(property=property_obj)

            for img in images:
                img.fixed_path = img.image.path.replace("\\", "/")

            comps.append({
                "property": property_obj,
                "form": comp_forms[pid],
                "images": images,
            })

    if not comps:
        return HttpResponse("No comps available for PDF.")

    html = render_to_string("properties/comp_pdf_all.html", {
        "comps": comps,
    })

    options = {"enable-local-file-access": True}

    pdf = pdfkit.from_string(html, False, options=options)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=comps_all.pdf"

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

# ============================================================
# PROPERTY NEW (DATABASE EDITOR)
# ============================================================
def property_new(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            prop = form.save()
            formset = PropertyImageFormSet(request.POST, request.FILES, instance=prop)
            if formset.is_valid():
                formset.save()
            return redirect("property_edit", property_id=prop.id)
    else:
        form = PropertyForm()
        # For new property, formset must be bound to a dummy instance
        dummy = Property()
        formset = PropertyImageFormSet(instance=dummy)

    return render(request, "properties/property_edit.html", {
        "form": form,
        "formset": formset,
        "property": None,
        "is_new": True,
    })


# ============================================================
# PROPERTY EDIT (DATABASE EDITOR)
# ============================================================
def property_edit(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    if request.method == "POST":
        form = PropertyForm(request.POST, instance=prop)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=prop)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("property_edit", property_id=prop.id)
    else:
        form = PropertyForm(instance=prop)
        formset = PropertyImageFormSet(instance=prop)

    return render(request, "properties/property_edit.html", {
        "form": form,
        "formset": formset,
        "property": prop,
        "is_new": False,
    })
# ============================================================
# PROPERTY RECORDS (DATABASE LIST)
# ============================================================
def property_records(request):
    properties = Property.objects.filter(deleted=False)
    return render(request, "properties/records.html", {
        "properties": properties,
    })

# ============================================================
# DELETE PROPERTY
# ============================================================
def property_delete(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    # Soft delete instead of hard delete
    prop.deleted = True
    prop.save()

    return redirect("property_records")

# ============================================================
# RECYCLE BIN — VIEW DELETED PROPERTIES
# ============================================================
def property_recycle_bin(request):
    deleted_properties = Property.objects.filter(deleted=True)
    return render(request, "properties/recycle_bin.html", {
        "properties": deleted_properties,
    })


# ============================================================
# DUPLICATE PROPERTY
# ============================================================
def property_duplicate(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    # Duplicate the property record
    new_prop = Property.objects.create(
        location=prop.location,
        county=prop.county,
        access=prop.access,
        size=prop.size,
        sqft=prop.sqft,
        utilities=prop.utilities,
        water=prop.water,
        improvements=prop.improvements,
        eco=prop.eco,
        terrain=prop.terrain,
        restrictions=prop.restrictions,
        price=prop.price,
        sale_date=prop.sale_date,
        grantor=prop.grantor,
        grantee=prop.grantee,
        document_no=prop.document_no,
        terms=prop.terms,
        listing=prop.listing,
        broker=prop.broker,
        verified_to=prop.verified_to,
        verified_by=prop.verified_by,
        verified_date=prop.verified_date,
        inspected_by=prop.inspected_by,
        inspected_date=prop.inspected_date,
        appraiser_name=prop.appraiser_name,
        comments=prop.comments,
    )

    # Duplicate images
    for img in prop.images.all():
        new_img = PropertyImage.objects.create(
            property=new_prop,
            caption=img.caption,
        )
        new_img.image.save(img.image.name, img.image.file, save=True)

    return redirect("property_edit", property_id=new_prop.id)

# ============================================================
# RESTORE PROPERTY (UNDO SOFT DELETE)
# ============================================================
def property_restore(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    prop.deleted = False
    prop.save()
    return redirect("property_recycle_bin")


# ============================================================
# HARD DELETE (PERMANENT)
# ============================================================
def property_hard_delete(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    prop.delete()  # permanent delete
    return redirect("property_recycle_bin")

# ============================================================
# EXPORT ALL PROPERTIES TO CSV
# ============================================================
import csv
from django.http import HttpResponse

def export_properties_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=properties.csv"

    writer = csv.writer(response)
    writer.writerow([
        "ID", "Location", "County", "Access", "Size", "SQFT",
        "Utilities", "Water", "Improvements", "Eco", "Terrain",
        "Restrictions", "Sale Price", "Sale Date", "Grantor", "Grantee",
        "Document No", "Terms", "Listing", "Broker",
        "Verified To", "Verified By", "Verified Date",
        "Inspected By", "Inspected Date", "Appraiser Name",
        "Comments"
    ])

    for p in Property.objects.filter(deleted=False):
        writer.writerow([
            p.id,
            p.location,
            p.county,
            p.access,
            p.size,
            p.sqft,
            p.utilities,
            p.water,
            p.improvements,
            p.eco,
            p.terrain,
            p.restrictions,
            p.sale_price,
            p.sale_date,
            p.grantor,
            p.grantee,
            p.bk_pg,            # ✔ correct field
            p.terms,
            p.listing,
            p.broker,
            p.verified_to,
            p.verified_by,
            p.verified_date,
            p.inspected_by,
            p.inspected_date,
            p.appraiser_name,
            p.comments,
        ])

    return response


# ============================================================
# EXPORT ALL COMPS TO CSV
# ============================================================
def export_comps_csv(request):
    comp_forms = request.session.get("comp_forms", {})
    selected = request.session.get("selected_comps", [])

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=comps.csv"

    writer = csv.writer(response)
    writer.writerow([
        "Comp Number", "Location", "County", "Access", "Size", "SQFT",
        "Utilities", "Water", "Improvements", "Eco", "Terrain",
        "Restrictions", "Price", "Sale Date", "Price Per Acre",
        "Grantor", "Grantee", "Document No", "Terms", "Listing",
        "Broker", "Verified To", "Verified By", "Verified Date",
        "Inspected By", "Inspected Date", "Appraiser Name",
        "Comments"
    ])

    for cid in selected:
        pid = str(cid)
        if pid in comp_forms:
            c = comp_forms[pid]
            writer.writerow([
                c.get("comp_number"),
                c.get("location"),
                c.get("county"),
                c.get("access"),
                c.get("size"),
                c.get("sqft"),
                c.get("utilities"),
                c.get("water"),
                c.get("improvements"),
                c.get("eco"),
                c.get("terrain"),
                c.get("restrictions"),
                c.get("price"),
                c.get("sale_date"),
                c.get("price_per_acre"),
                c.get("grantor"),
                c.get("grantee"),
                c.get("document_no"),
                c.get("terms"),
                c.get("listing"),
                c.get("broker"),
                c.get("verified_to"),
                c.get("verified_by"),
                c.get("verified_date"),
                c.get("inspected_by"),
                c.get("inspected_date"),
                c.get("appraiser_name"),
                c.get("comments"),
            ])

    return response


# ============================================================
# NAVIGATION DASHBOARD VIEW
# ============================================================
def navigation(request):
    return render(request, "properties/navigation.html")

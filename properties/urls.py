from django.urls import path
from .views import (
    property_search,
    comp_list,
    comp_edit,
    comp_preview,
    comp_start,
    comp_pdf,
    comp_pdf_all,
    property_new,
    property_edit,
    property_delete,
    property_duplicate,
    export_properties_csv,
    export_comps_csv,
    navigation,
    property_records,
    property_recycle_bin,     # ← FIXED
    property_restore,         # ← FIXED
    property_hard_delete,     # ← FIXED
)

urlpatterns = [
    # Navigation Dashboard
    path("nav/", navigation, name="navigation"),

    # Search page
    path("", property_search, name="property_search"),

    # Multi-comp workflow
    path("comp/list/", comp_list, name="comp_list"),
    path("comp/start/", comp_start, name="comp_start"),
    path("comp/<int:property_id>/", comp_edit, name="comp_edit"),

    # Single-comp PDF
    path("comp/<int:property_id>/pdf/", comp_pdf, name="comp_pdf"),

    # Multi-comp PDF (ALL comps)
    path("comp/pdf/all/", comp_pdf_all, name="comp_pdf_all"),

    # Preview all comps
    path("comp/preview/", comp_preview, name="comp_preview"),

    # Database editor
    path("property/new/", property_new, name="property_new"),
    path("property/<int:property_id>/edit/", property_edit, name="property_edit"),

    # Database Records (LIST VIEW)
    path("records/", property_records, name="property_records"),

    # Recycle Bin + Restore + Hard Delete
    path("records/deleted/", property_recycle_bin, name="property_recycle_bin"),
    path("property/<int:property_id>/restore/", property_restore, name="property_restore"),
    path("property/<int:property_id>/hard_delete/", property_hard_delete, name="property_hard_delete"),

    # Delete + Duplicate
    path("property/<int:property_id>/delete/", property_delete, name="property_delete"),
    path("property/<int:property_id>/duplicate/", property_duplicate, name="property_duplicate"),

    # CSV Export
    path("export/properties/", export_properties_csv, name="export_properties_csv"),
    path("export/comps/", export_comps_csv, name="export_comps_csv"),
]

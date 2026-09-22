from django import forms
from django.forms import inlineformset_factory
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            # Basic info
            "location",
            "county",
            "access",
            "sqft",

            # Size / physical
            "size",
            "utilities",
            "water",
            "improvements",
            "eco",
            "terrain",
            "restrictions",

            # Sale info
            "sale_price",
            "sale_date",
            "terms",
            "listing",
            "broker",

            # Parties / docs
            "grantor",
            "grantee",
            "bk_pg",

            # Verification / inspection
            "verified_to",
            "verified_by",
            "verified_date",
            "inspected_by",
            "inspected_date",
            "appraiser_name",

            # Comments
            "comments",
        ]

        widgets = {
            "sale_date": forms.DateInput(attrs={"type": "date"}),
            "verified_date": forms.DateInput(attrs={"type": "date"}),
            "inspected_date": forms.DateInput(attrs={"type": "date"}),
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ["image", "caption"]

PropertyImageFormSet = inlineformset_factory(
    Property,
    PropertyImage,
    form=PropertyImageForm,
    extra=2,            # show 2 empty upload slots
    can_delete=True,
    min_num=0,          # allow zero images
    validate_min=False  # do NOT require all extra forms to be filled
)

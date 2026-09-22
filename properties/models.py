from django.db import models

class Property(models.Model):
    # Access primary key
    access_id = models.IntegerField(null=True, blank=True)  # ID

    # Basic info
    datano = models.CharField(max_length=50, null=True, blank=True)  # DATANO
    location = models.CharField(max_length=255, null=True, blank=True)  # LOCATION
    address = models.CharField(max_length=255, null=True, blank=True)
    county = models.CharField(max_length=100, null=True, blank=True)  # COUNTY
    zone = models.CharField(max_length=50, null=True, blank=True)  # ZONE
    sqft = models.CharField(max_length=50, null=True, blank=True)  # SQFT

    # Size fields
    size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # SIZE (Acres)
    size_total_acres = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # SizeTotalAcres
    deeded_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Deeded Size
    nmsl_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # NMSL Size
    slo_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # SLO Size
    blm_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # BLM Size

    # Sale info
    sale_date = models.DateField(null=True, blank=True)  # SALEDATE
    sale_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)  # PRICE
    price_per_acre = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)  # PricePerAcre
    terms = models.CharField(max_length=255, null=True, blank=True)  # TERMS
    dom = models.IntegerField(null=True, blank=True)  # DOM
    listing = models.CharField(max_length=255, null=True, blank=True)  # LISTING
    broker = models.CharField(max_length=255, null=True, blank=True)  # BROKER
    resale_of = models.CharField(max_length=255, null=True, blank=True)  # RESALE_OF
    previous_sp = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)  # PREVIOUSSP
    listing_date = models.DateField(null=True, blank=True)  # LISTING_DATE
    condition_of_sale = models.CharField(max_length=255, null=True, blank=True)  # CONDITION_OF_SALE
    previous_sale_date = models.DateField(null=True, blank=True)  # PREVIOUS_SALE_DATE

    # Parties / docs
    grantor = models.CharField(max_length=255, null=True, blank=True)  # GRANTOR
    grantee = models.CharField(max_length=255, null=True, blank=True)  # GRANTEE
    doc = models.CharField(max_length=255, null=True, blank=True)  # DOC
    bk_pg = models.CharField(max_length=255, null=True, blank=True)  # BK_PG

    # Site / physical
    road_st = models.CharField(max_length=255, null=True, blank=True)  # ROAD_ST
    access = models.CharField(max_length=255, null=True, blank=True)  # ACCESS
    utilities = models.CharField(max_length=255, null=True, blank=True)  # UTILITIES
    water = models.CharField(max_length=255, null=True, blank=True)  # WATER
    waterright = models.CharField(max_length=255, null=True, blank=True)  # WATERRIGHT
    minerals = models.CharField(max_length=255, null=True, blank=True)  # MINERALS
    pres_use = models.CharField(max_length=255, null=True, blank=True)  # PRES_USE
    best_use = models.CharField(max_length=255, null=True, blank=True)  # BESTUSE
    improvements = models.CharField(max_length=255, null=True, blank=True)  # IMPROV
    eco = models.CharField(max_length=255, null=True, blank=True)  # ECO
    terrain = models.CharField(max_length=255, null=True, blank=True)  # TERRAIN
    restrictions = models.CharField(max_length=255, null=True, blank=True)  # RESTRICTIONS
    leases_permits = models.CharField(max_length=255, null=True, blank=True)  # LEASES/PERMITS
    buyer_motivation = models.CharField(max_length=255, null=True, blank=True)  # BUYER_MOTIVATION

    # Legal / mapping
    legal = models.TextField(null=True, blank=True)  # LEGAL
    section = models.CharField(max_length=50, null=True, blank=True)  # SECTION
    township = models.CharField(max_length=50, null=True, blank=True)  # TOWNSHIP
    range = models.CharField(max_length=50, null=True, blank=True)  # RANGE
    tract = models.CharField(max_length=50, null=True, blank=True)  # TRACT
    map_ref = models.CharField(max_length=255, null=True, blank=True)  # MAP
    survey = models.CharField(max_length=255, null=True, blank=True)  # SURVEY
    tax_idnum = models.CharField(max_length=255, null=True, blank=True)  # TAX_IDNUM
    subdivision = models.CharField(max_length=255, null=True, blank=True)  # SUBDIVISION
    lotnum = models.CharField(max_length=255, null=True, blank=True)  # LOTNUM

    # Verification / inspection
    verified_to = models.CharField(max_length=255, null=True, blank=True)  # VERI_TO
    verified_by = models.CharField(max_length=255, null=True, blank=True)  # VERI_BY
    verified_date = models.DateField(null=True, blank=True)  # VERI_DATE
    inspected_by = models.CharField(max_length=255, null=True, blank=True)  # INSP
    inspected_date = models.DateField(null=True, blank=True)  # INSP_DATE
    appraiser_name = models.CharField(max_length=255, null=True, blank=True)  # APPRNAME

    # Analysis / comments
    analysis = models.TextField(null=True, blank=True)  # ANALYSIS
    analysis2 = models.TextField(null=True, blank=True)  # ANALYSIS2
    analysis3 = models.TextField(null=True, blank=True)  # ANALYSIS3
    comments = models.TextField(null=True, blank=True)  # COMMENTS

    # Misc / links
    file_reference = models.CharField(max_length=255, null=True, blank=True)  # FILE_REFERENCE
    pmhlink = models.CharField(max_length=255, null=True, blank=True)  # PMHLINK
    pmhlinkaddr = models.CharField(max_length=255, null=True, blank=True)  # PMHLINKADDR
    datasource = models.CharField(max_length=255, null=True, blank=True)  # DATASOURCE

    # Soft Delete
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.access_id} – {self.address or self.location}"


class PropertyDraft(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    updated_comments = models.TextField(null=True, blank=True)
    updated_dom = models.IntegerField(null=True, blank=True)
    updated_sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Draft for {self.property.address}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    label = models.CharField(max_length=50, null=True, blank=True)

    # NEW FIELD (requested)
    caption = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.property.id} → {self.image.name}"

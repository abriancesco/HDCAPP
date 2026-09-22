import csv
import os

from django.core.management.base import BaseCommand
from properties.models import Property


class Command(BaseCommand):
    help = "Rebuild Property table from landata1.csv (Access export)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="landata1.csv",
            help="Path to landata1.csv (Access export)",
        )

    def handle(self, *args, **options):
        path = options["path"]

        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return

        self.stdout.write(self.style.WARNING("Deleting all existing Property rows..."))
        Property.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f"Importing from {path}..."))

        created = 0

        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=",")

            for row in reader:
                try:
                    # Helper functions
                    def dec(name):
                        val = row.get(name, "").strip()
                        if not val:
                            return None
                        try:
                            return float(val.replace(",", ""))
                        except:
                            return None

                    def intval(name):
                        val = row.get(name, "").strip()
                        if not val:
                            return None
                        try:
                            return int(val)
                        except:
                            return None

                    def text(name):
                        val = row.get(name, "").strip()
                        return val or None

                    def dateval(name):
                        val = row.get(name, "").strip()
                        if not val:
                            return None
                        return val  # raw string, Django will parse later

                    # Create property
                    p = Property(
                        access_id=intval("ID"),
                        datano=text("DATANO"),
                        location=text("LOCATION"),
                        address=text("LOCATION"),
                        county=text("COUNTY"),
                        zone=text("ZONE"),
                        sqft=text("SQFT"),

                        # Updated size field name
                        size=dec("SIZE"),
                        size_total_acres=dec("SizeTotalAcres"),
                        deeded_size=dec("Deeded Size"),
                        nmsl_size=dec("NMSL Size"),
                        slo_size=dec("SLO Size"),
                        blm_size=dec("BLM Size"),

                        sale_date=dateval("SALEDATE"),
                        sale_price=dec("PRICE"),
                        price_per_acre=dec("PricePerAcre"),
                        terms=text("TERMS"),
                        dom=intval("DOM"),
                        listing=text("LISTING"),
                        broker=text("BROKER"),
                        resale_of=text("RESALE_OF"),
                        previous_sp=dec("PREVIOUSSP"),
                        listing_date=dateval("LISTING_DATE"),
                        condition_of_sale=text("CONDITION_OF_SALE"),
                        previous_sale_date=dateval("PREVIOUS_SALE_DATE"),

                        grantor=text("GRANTOR"),
                        grantee=text("GRANTEE"),
                        doc=text("DOC"),
                        bk_pg=text("BK_PG"),

                        road_st=text("ROAD_ST"),
                        access=text("ACCESS"),
                        utilities=text("UTILITIES"),
                        water=text("WATER"),
                        waterright=text("WATERRIGHT"),
                        minerals=text("MINERALS"),
                        pres_use=text("PRES_USE"),
                        best_use=text("BESTUSE"),

                        # Updated field name
                        improvements=text("IMPROV"),

                        eco=text("ECO"),
                        terrain=text("TERRAIN"),
                        restrictions=text("RESTRICTIONS"),
                        leases_permits=text("LEASES/PERMITS"),
                        buyer_motivation=text("BUYER_MOTIVATION"),

                        legal=text("LEGAL"),
                        section=text("SECTION"),
                        township=text("TOWNSHIP"),
                        range=text("RANGE"),
                        tract=text("TRACT"),
                        map_ref=text("MAP"),
                        survey=text("SURVEY"),
                        tax_idnum=text("TAX_IDNUM"),
                        subdivision=text("SUBDIVISION"),
                        lotnum=text("LOTNUM"),

                        # Updated verification field names
                        verified_to=text("VERI_TO"),
                        verified_by=text("VERI_BY"),
                        verified_date=dateval("VERI_DATE"),
                        inspected_by=text("INSP"),
                        inspected_date=dateval("INSP_DATE"),
                        appraiser_name=text("APPRNAME"),

                        analysis=text("ANALYSIS"),
                        analysis2=text("ANALYSIS2"),
                        analysis3=text("ANALYSIS3"),
                        comments=text("COMMENTS"),

                        file_reference=text("FILE_REFERENCE"),
                        pmhlink=text("PMHLINK"),
                        pmhlinkaddr=text("PMHLINKADDR"),
                        datasource=text("DATASOURCE"),
                    )

                    p.save()
                    created += 1

                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error on row with ID={row.get('ID')}: {e}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS(f"Import complete. Created {created} properties."))

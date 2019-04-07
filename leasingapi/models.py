# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models, connection
from django.utils import timezone
import binascii


def _create_hash():
    return binascii.hexlify(os.urandom(32))


def _create_short_hash():
    return binascii.hexlify(os.urandom(32))


class ClientSetting(models.Model):
    country_choices = (("AUS", "AUSTRALIA"),
                       ("UK", "UNITED KINGDOM"),
                       ("US", "UNITED STATES"),
                       ("NZ", "NEW ZEALAND"),
                       ("CAN", "CANADA"))

    state_choices = (("NSW", "NEW SOUTH WALES"),
                     ("ACT", "AUSTRALIAN CAPITAL TERITORY"),
                     ("NT", "NORTHERN TERITORY"),
                     ("QLD", "QUEENSLAND"),
                     ("SA", "SOUTH AUSTRALIA"),
                     ("TAS", "TASMANIA"),
                     ("VIC", "VICTORIA"),
                     ("WA", "WESTERN AUSTRALIA"),
                     ("AL", "ALABAMA"),
                     ("AK", "ALASKA"),
                     ("AZ", "ARIZONA"),
                     ("AR", "ARKANSAS"),
                     ("CA", "CALIFORNIA"),
                     ("CO", "COLORADO"),
                     ("CT", "CONNECTICUT"),
                     ("DE", "DELAWARE"),
                     ("FL", "FLORIDA"),
                     ("GA", "GEORGIA"),
                     ("HI", "HAWAII"),
                     ("ID", "IDAHO"),
                     ("IL", "ILLINOIS"),
                     ("IN", "INDIANA"),
                     ("IA", "IOWA"),
                     ("KS", "KANSAS"),
                     ("KY", "KENTUCKY"),
                     ("LA", "LOUISIANA"),
                     ("ME", "MAINE"),
                     ("MD", "MARYLAND"),
                     ("MA", "MASSACHUSETTS"),
                     ("MI", "MICHIGAN"),
                     ("MN", "MINNESOTA"),
                     ("MS", "MISSISSIPPI"),
                     ("MO", "MISSOURI"),
                     ("MT", "MONTANA"),
                     ("NE", "NEBRASKA"),
                     ("NV", "NEVADA"),
                     ("NH", "NEW HAMPSHIRE"),
                     ("NJ", "NEW JERSEY"),
                     ("NM", "NEW MEXICO"),
                     ("NY", "NEW YORK"),
                     ("NC", "NORTH CAROLINA"),
                     ("ND", "NORTH DAKOTA"),
                     ("OH", "OHIO"), ("OKLAHOMA", "OKLAHOMA"),
                     ("OR", "OREGON"),
                     ("PA", "PENNSYLVANIA"),
                     ("RI", "RHODE ISLAND"),
                     ("SC", "SOUTH CAROLINA"),
                     ("SD", "SOUTH DAKOTA"),
                     ("TN", "TENNESSEE"),
                     ("TX", "TEXAS"),
                     ("UT", "UTAH"),
                     ("VT", "VERMONT"),
                     ("VA", "VIRGINIA"),
                     ("WA", "WASHINGTON"),
                     ("WV", "WEST VIRGINIA"),
                     ("WI", "WISCONSIN"),
                     ("WY", "WYOMING"),
                     ("ENG", "ENGLAND"),
                     ("NIR", "NORTHERN IRELAND"),
                     ("SCO", "SCOTLAND"),
                     ("WAL", "WALES"),
                     ("NZ-AUK", "AUCKLAND"),
                     ("NZ-BOP", "BAY OF PLENTY"),
                     ("NZ-CAN", "CANTERBURY"),
                     ("NZ-GIS", "GISBORNE"),
                     ("NZ-HKB", "HAWKE'S BAY"),
                     ("NZ-MBH", "MARLBOROUGH"),
                     ("NZ-MWT", "ANAWATU-WANGANUI"),
                     ("NZ-NSN", "NELSON"),
                     ("NZ-NTL", "NORTH LAND"),
                     ("NZ-OTA", "OTAGO"),
                     ("NZ-STL", "SOUTH LAND"),
                     ("NZ-TAS", "TASMAN"),
                     ("NZ-TKI", "TARANAKI"),
                     ("NZ-WKO", "WAIKATO"),
                     ("NZ-WGN", "WELLINGTON"),
                     ("NZ-WTC", "WEST COAST"),
                     ("NZ-CIT", "CHATHAM ISLANDS TERRITORY"),
                     ("AB", "ALBERTA"),
                     ("BC", "BRITISH COLUMBIA"),
                     ("MB", "MANITOBA"),
                     ("NB", "NEW BRUNSWICK"),
                     ("NL", "NEWFOUNDLAND AND LABRADOR"),
                     ("NT", "NORTHWEST TERRITORIES"),
                     ("NS", "NOVA SCOTIA"),
                     ("NU", "NUNAVUT"),
                     ("ON", "ONTARIO"),
                     ("PE", "PRINCE EDWARD ISLAND"),
                     ("QC", "QUEBEC"),
                     ("SK", "SASKATCHEWAN"),
                     ("YT", "YUKON"))

    representing_choice_fields = (("TNT", "TENANT"),
                                  ("LND", "LANDLORD"))

    country = models.CharField(max_length=3, choices=country_choices,
                               default='AUS', null=False, blank=False)
    state = models.CharField(max_length=6, choices=state_choices,
                             default="NSW", null=False, blank=False)
    representing = models.CharField(max_length=3,
                                    choices=representing_choice_fields,
                                    default="TNT", null=False, blank=False)
    client = models.ForeignKey('leasingauth.LeasingClient',
                               related_name="client_settings",
                               null=False, blank=False,
                               on_delete=models.CASCADE)

    def __str__(self):
        return "#%s- COUNTRY (%s), STATE (%s), REP (%s) " % (self.id,
                                                             self.country,
                                                             self.state,
                                                             self.representing)

    class Meta:
        verbose_name_plural = "Client Settings"


class DocumentUpload(models.Model):
    client = models.ForeignKey('leasingauth.LeasingClient',
                               related_name="document_uploads",
                               on_delete=models.CASCADE)
    document = models.FileField(upload_to="client_documents/")
    upload_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s - %s" % (self.id, self.document.name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            cursor = connection.cursor()
            cursor.execute("select nextval('leasingapi_documentupload_id_seq')")  # NOQA
            result = cursor.fetchone()
            if result:
                self.id = int(result[0])
            else:
                self.id = 1
            if self.document:
                document_extension = self.document.name.split('.')[-1]
                self.document.name = '%s-%s.%s' % (self.id,
                                                   _create_short_hash(),
                                                   document_extension)
                super(DocumentUpload, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Document Uploads'


class ExportResult(models.Model):
    ammend_number = models.TextField(null=True, blank=True)
    clause_number = models.TextField(null=False, blank=False)
    clause_name = models.TextField(null=False, blank=False)
    Lease_required_amendment = models.TextField(null=True, blank=True)
    lessor_response = models.TextField(null=True, blank=True) 

    def __str__(self):
        return '%s' % (self.clause_number)


class KeyText(models.Model):
    """
    Django Model used to store the key text related to legal positions
    """
    content = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        if len(self.content) > 30:
            return "%s..." % self.content[:30]
        else:
            return self.content


class Description(models.Model):
    text = models.TextField(null=False, blank=False)

    def __str__(self):
        return "%s - %s" % (self.id,self.text)


class LegalPosition(models.Model):
    switch_choices = (('NFD', 'Not Found'),
                      ('FND', 'Found'))
    client = models.ForeignKey('leasingauth.LeasingUser',
                               related_name="legal_positions",
                               on_delete=models.CASCADE)
    export_result = models.ForeignKey(ExportResult,
                                      related_name="export_result",
                                      null=True, blank=True,
                                      on_delete=models.SET_NULL)
    clause_name = models.ManyToManyField(Description,
                                         related_name="clause_description")
    text = models.ManyToManyField(KeyText, related_name="legal_positions")
    reason = models.TextField(null=False, blank=False)
    setting = models.ForeignKey(ClientSetting, related_name="client_setting",
                                null=True, blank=True,
                                on_delete=models.SET_NULL)
    action = models.CharField(max_length=3, choices=switch_choices,
                              default='NFD')
    document = models.ForeignKey(DocumentUpload,
                                 related_name="legal_positions",
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return "#%s - %s" % (self.id, self.clause_name)

    class Meta:
        verbose_name_plural = 'Legal Positions'

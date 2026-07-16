from django.contrib.auth.models import AbstractUser
from django.db import models


# 50+ world currencies covering every major region
CURRENCY_CHOICES = [
    # Americas
    ('USD', 'USD — US Dollar ($)'),
    ('CAD', 'CAD — Canadian Dollar (CA$)'),
    ('BRL', 'BRL — Brazilian Real (R$)'),
    ('MXN', 'MXN — Mexican Peso (MX$)'),
    ('ARS', 'ARS — Argentine Peso ($)'),
    ('CLP', 'CLP — Chilean Peso ($)'),
    ('COP', 'COP — Colombian Peso ($)'),
    ('PEN', 'PEN — Peruvian Sol (S/)'),
    # Europe
    ('EUR', 'EUR — Euro (€)'),
    ('GBP', 'GBP — British Pound (£)'),
    ('CHF', 'CHF — Swiss Franc (Fr)'),
    ('SEK', 'SEK — Swedish Krona (kr)'),
    ('NOK', 'NOK — Norwegian Krone (kr)'),
    ('DKK', 'DKK — Danish Krone (kr)'),
    ('PLN', 'PLN — Polish Zloty (zł)'),
    ('CZK', 'CZK — Czech Koruna (Kč)'),
    ('HUF', 'HUF — Hungarian Forint (Ft)'),
    ('RON', 'RON — Romanian Leu (lei)'),
    ('TRY', 'TRY — Turkish Lira (₺)'),
    ('RUB', 'RUB — Russian Ruble (₽)'),
    ('UAH', 'UAH — Ukrainian Hryvnia (₴)'),
    # Africa
    ('NGN', 'NGN — Nigerian Naira (₦)'),
    ('ZAR', 'ZAR — South African Rand (R)'),
    ('KES', 'KES — Kenyan Shilling (KSh)'),
    ('GHS', 'GHS — Ghanaian Cedi (₵)'),
    ('EGP', 'EGP — Egyptian Pound (£)'),
    ('ETB', 'ETB — Ethiopian Birr (Br)'),
    ('TZS', 'TZS — Tanzanian Shilling (TSh)'),
    ('UGX', 'UGX — Ugandan Shilling (USh)'),
    ('MAD', 'MAD — Moroccan Dirham (MAD)'),
    ('XOF', 'XOF — West African CFA Franc (CFA)'),
    ('XAF', 'XAF — Central African CFA Franc (CFA)'),
    # Middle East
    ('AED', 'AED — UAE Dirham (د.إ)'),
    ('SAR', 'SAR — Saudi Riyal (﷼)'),
    ('QAR', 'QAR — Qatari Riyal (﷼)'),
    ('ILS', 'ILS — Israeli Shekel (₪)'),
    # Asia & Pacific
    ('JPY', 'JPY — Japanese Yen (¥)'),
    ('CNY', 'CNY — Chinese Yuan (¥)'),
    ('INR', 'INR — Indian Rupee (₹)'),
    ('KRW', 'KRW — South Korean Won (₩)'),
    ('HKD', 'HKD — Hong Kong Dollar (HK$)'),
    ('SGD', 'SGD — Singapore Dollar (S$)'),
    ('TWD', 'TWD — Taiwan Dollar (NT$)'),
    ('THB', 'THB — Thai Baht (฿)'),
    ('MYR', 'MYR — Malaysian Ringgit (RM)'),
    ('IDR', 'IDR — Indonesian Rupiah (Rp)'),
    ('PHP', 'PHP — Philippine Peso (₱)'),
    ('VND', 'VND — Vietnamese Dong (₫)'),
    ('PKR', 'PKR — Pakistani Rupee (₨)'),
    ('BDT', 'BDT — Bangladeshi Taka (৳)'),
    ('AUD', 'AUD — Australian Dollar (A$)'),
    ('NZD', 'NZD — New Zealand Dollar (NZ$)'),
]

TIMEZONE_CHOICES = [
    # Americas
    ('America/New_York',      'New York (EST/EDT)'),
    ('America/Chicago',       'Chicago (CST/CDT)'),
    ('America/Denver',        'Denver (MST/MDT)'),
    ('America/Los_Angeles',   'Los Angeles (PST/PDT)'),
    ('America/Toronto',       'Toronto (EST/EDT)'),
    ('America/Vancouver',     'Vancouver (PST/PDT)'),
    ('America/Sao_Paulo',     'São Paulo (BRT)'),
    ('America/Mexico_City',   'Mexico City (CST/CDT)'),
    ('America/Buenos_Aires',  'Buenos Aires (ART)'),
    ('America/Bogota',        'Bogotá (COT)'),
    ('America/Lima',          'Lima (PET)'),
    ('America/Santiago',      'Santiago (CLT)'),
    # Europe
    ('Europe/London',         'London (GMT/BST)'),
    ('Europe/Paris',          'Paris (CET/CEST)'),
    ('Europe/Berlin',         'Berlin (CET/CEST)'),
    ('Europe/Madrid',         'Madrid (CET/CEST)'),
    ('Europe/Rome',           'Rome (CET/CEST)'),
    ('Europe/Amsterdam',      'Amsterdam (CET/CEST)'),
    ('Europe/Zurich',         'Zurich (CET/CEST)'),
    ('Europe/Stockholm',      'Stockholm (CET/CEST)'),
    ('Europe/Warsaw',         'Warsaw (CET/CEST)'),
    ('Europe/Istanbul',       'Istanbul (TRT)'),
    ('Europe/Moscow',         'Moscow (MSK)'),
    ('Europe/Kiev',           'Kyiv (EET/EEST)'),
    # Africa
    ('Africa/Lagos',          'Lagos (WAT)'),
    ('Africa/Nairobi',        'Nairobi (EAT)'),
    ('Africa/Johannesburg',   'Johannesburg (SAST)'),
    ('Africa/Cairo',          'Cairo (EET)'),
    ('Africa/Accra',          'Accra (GMT)'),
    ('Africa/Addis_Ababa',    'Addis Ababa (EAT)'),
    ('Africa/Dar_es_Salaam',  'Dar es Salaam (EAT)'),
    ('Africa/Casablanca',     'Casablanca (WET)'),
    ('Africa/Abidjan',        'Abidjan (GMT)'),
    ('Africa/Dakar',          'Dakar (GMT)'),
    # Middle East
    ('Asia/Dubai',            'Dubai (GST)'),
    ('Asia/Riyadh',           'Riyadh (AST)'),
    ('Asia/Qatar',            'Doha (AST)'),
    ('Asia/Jerusalem',        'Jerusalem (IST)'),
    # Asia & Pacific
    ('Asia/Tokyo',            'Tokyo (JST)'),
    ('Asia/Shanghai',         'Shanghai (CST)'),
    ('Asia/Kolkata',          'Mumbai/Delhi (IST)'),
    ('Asia/Seoul',            'Seoul (KST)'),
    ('Asia/Hong_Kong',        'Hong Kong (HKT)'),
    ('Asia/Singapore',        'Singapore (SGT)'),
    ('Asia/Taipei',           'Taipei (CST)'),
    ('Asia/Bangkok',          'Bangkok (ICT)'),
    ('Asia/Kuala_Lumpur',     'Kuala Lumpur (MYT)'),
    ('Asia/Jakarta',          'Jakarta (WIB)'),
    ('Asia/Manila',           'Manila (PHT)'),
    ('Asia/Karachi',          'Karachi (PKT)'),
    ('Asia/Dhaka',            'Dhaka (BST)'),
    ('Australia/Sydney',      'Sydney (AEST/AEDT)'),
    ('Australia/Melbourne',   'Melbourne (AEST/AEDT)'),
    ('Pacific/Auckland',      'Auckland (NZST/NZDT)'),
    ('UTC',                   'UTC'),
]

# Currency symbol map for display
CURRENCY_SYMBOLS = {
    'USD':'$','EUR':'€','GBP':'£','JPY':'¥','CNY':'¥','INR':'₹',
    'KRW':'₩','BRL':'R$','RUB':'₽','TRY':'₺','NGN':'₦','GHS':'₵',
    'ZAR':'R','KES':'KSh','EGP':'£','ILS':'₪','THB':'฿','PHP':'₱',
    'VND':'₫','PKR':'₨','BDT':'৳','UAH':'₴','HUF':'Ft','PLN':'zł',
    'SEK':'kr','NOK':'kr','DKK':'kr','CHF':'Fr','CAD':'CA$','AUD':'A$',
    'NZD':'NZ$','HKD':'HK$','SGD':'S$','TWD':'NT$','MYR':'RM',
    'IDR':'Rp','AED':'د.إ','SAR':'﷼','QAR':'﷼','MXN':'MX$',
    'ARS':'$','CLP':'$','COP':'$','PEN':'S/','RON':'lei','CZK':'Kč',
    'ETB':'Br','TZS':'TSh','UGX':'USh','MAD':'MAD',
    'XOF':'CFA','XAF':'CFA',
}


class User(AbstractUser):
    preferred_currency = models.CharField(max_length=10, default='USD', choices=CURRENCY_CHOICES)
    timezone = models.CharField(max_length=60, default='UTC', choices=TIMEZONE_CHOICES)
    country = models.CharField(max_length=60, blank=True)
    is_premium = models.BooleanField(default=False)  # premium tier flag
    premium_since = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def currency_symbol(self):
        return CURRENCY_SYMBOLS.get(self.preferred_currency, self.preferred_currency)

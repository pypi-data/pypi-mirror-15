# Django UPS Time In Transit

django-ups-tnt is a wrapper around UPS's Time In Transit (TNT) API.

This wrapper is necessary because UPS's API is not public and requires Authentication details that cannot be shared
in javascript.

It provides some defaults to make the api easier to work with.
It also provides some form validation before hitting the UPS API and cache

# Installation

Requires djangorestframework>=3.3.0. Tested on Django 1.8 and 1.9.

1. Add `django-ups-tnt` to requirements.txt or pip install.
2. Add `url(r'^api/', include('ups_tnt.urls')),` to urls.py
3. Set required settings in settings.py

## Settings

### Required

UPS_USERNAME

UPS_PASSWORD

UPS_ACCESS_LICENSE_NUMBER

### Override defaults

UPS_DEFAULT_SHIP_FROM  
UPS_DEFAULT_SHIP_TO

Default shipping addresses

Example syntax:

```
{
    "Address": {
        "CountryCode": "US",
    }
}
```

UPS_BUFFER_DAYS - add buffer to when the item is shipped. Defaults to 0. Set to a int or callable.

UPS_DEFAULT_SHIPMENT_WEIGHT - Set shipment weight. Example

```
UPS_DEFAULT_SHIPMENT_WEIGHT = {
    "UnitOfMeasurement": {
        "Code": "LBS",
        "Description": "Pounds"
    },
    "Weight": "90"
}
```

UPS_DEFAULT_INVOICE - Set value of shipment

```
UPS_DEFAULT_INVOICE = {
    "CurrencyCode": "USD",
    "MonetaryValue": "800"
}
```

UPS_TEST_LIVE - Set to `True` to make unit tests access actual API instead of mocks

UPS_CACHE_NAME - Set to the name of the cache to use. Defaults to `default`

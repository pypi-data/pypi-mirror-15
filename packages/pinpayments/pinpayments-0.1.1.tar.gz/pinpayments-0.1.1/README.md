PinPayments Python
=======================

PinPayments-Python is a Python interface to the [Pin Payments](https://pin.net.au/docs/api)
API

## Installation:

```
pip install pinpayments
```

## Quickstart:

```
python
>>> from pinpayments import PinPayments
>>> api_secret = <api_secret>
>>> pin = PinPayments(api_secret = api_secret, test = False)
>>> customers = pin.getCustomers()
```

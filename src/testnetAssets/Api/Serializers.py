


from rest_framework import serializers
from stellar_sdk.account import Account
from django.core.exceptions import ValidationError
from stellar_sdk.asset import Asset
from stellar_sdk.exceptions import AssetCodeInvalidError, AssetIssuerInvalidError


def check_stellar_address(value):
    try:
        Account(account=value, sequence=0)
    except ValueError:
        raise ValidationError("Invalid Stellar Address")
    else:
        return value
def check_asset_code(value):
    try:
        Asset(value, None)
    except AssetCodeInvalidError:
        raise ValidationError("Invalid stellar asset code, should be between 3-12 characters long")
    except AssetIssuerInvalidError:
        return value
    else:
        return value

class AssetsSerializer(serializers.Serializer):
    code = serializers.CharField(validators=[check_asset_code]) #not including liquidity shares
   
   

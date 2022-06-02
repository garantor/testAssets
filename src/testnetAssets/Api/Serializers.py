


from rest_framework import serializers
from stellar_sdk.account import Account
from django.core.exceptions import ValidationError


def check_stellar_address(value):
    try:
        Account(account=value, sequence=0)
    except ValueError:
        raise ValidationError("Invalid Stellar Address")
    else:
        return value


class AssetsSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=3, max_length=12) #not including liquidity shares
    # issuer = serializers.CharField(
    #     min_length=56, max_length=56,  validators=[check_stellar_address])
   

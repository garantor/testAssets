from django.shortcuts import render
# from rest_framework import APIView, Response, status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Api.Serializers import AssetsSerializer
from Api.utils import create_Assets, is_asset_trusted, list_of_trusted_assets
from stellar_sdk.exceptions import BadRequestError, NotFoundError, BadResponseError



# Create your views here.

@api_view(['GET'])
def landingPage(request):
        # to include template for break down of all endpoints and their functions
       return Response({"msg":"ok",},status=status.HTTP_200_OK)

@api_view(['POST'])
def create_assets(request):
    if request.method == "POST":
        serializeRequest = AssetsSerializer(data=request.data)
        if serializeRequest.is_valid():
            asset_code = request.data.get('code')
            check_asset = is_asset_trusted(asset_code)
            if check_asset == True:
                resp = {"message":"an asset with this code already exist, please use that asset"}
                return Response(resp, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    asset_created = create_Assets(asset_code)
                except Exception as Error:
                    print(Error)
                    #notify admin
                    return Response({"error":"Error creating Asset"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if asset_created:
                    # except BadRequestError:
                    #     return Response({"msg":"Error creating Assets"},status=status.HTTP_400_BAD_REQUEST)
                        return Response(asset_created, status=status.HTTP_200_OK)
                    else:
                        return Response(asset_created, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializeRequest.errors,status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['GET'])
def reset_main_account(request):
    if request.method == "GET":
        from Api.utils import reset_main_account
        try:
            adc = reset_main_account()
        except Exception:
            return Response({"msg": "Account already reset"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "ok"}, status=status.HTTP_200_OK)

@api_view(["GET"])
def list_of_available_assets(request):
    if request.method == "GET":
        asset_list = list_of_trusted_assets()
        return Response(asset_list, status=status.HTTP_200_OK)
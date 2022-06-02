from xml.dom import ValidationErr
from django.shortcuts import render
# from rest_framework import APIView, Response, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Api.Serializers import AssetsSerializer
from Api.utils import create_Assets


# Create your views here.

@api_view(['GET'])
def landingPage(request):
        # to include template for break down of all endpoints and their functions
       return Response({"msg":"ok"},status=status.HTTP_200_OK)
@api_view(['POST'])
def create_assets(request):
    if request.method == "POST":
    
        serializeRequest = AssetsSerializer(data=request.data)
        if serializeRequest.is_valid():
            asset_code = request.data.get('code')
            asset_created = create_Assets(asset_code)
            return Response({"msg": asset_created}, status=status.HTTP_200_OK)
        else:
            return Response(serializeRequest.errors,status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['GET'])
def reset_main_account(request):
    if request.method == "GET":
        from Api.utils import reset_main_account
        
        adc = reset_main_account()
        if adc != None:
            return Response({"msg": "ok"}, status=status.HTTP_200_OK)
        return Response({"msg": "Account already reset"}, status=status.HTTP_400_BAD_REQUEST)

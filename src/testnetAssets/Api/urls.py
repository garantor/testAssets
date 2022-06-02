from .views import *
from django.urls import path, include

urlpatterns = [
    path('', landingPage),
    path('createAssets', create_assets),
    path('resetMainAccount', reset_main_account),
]

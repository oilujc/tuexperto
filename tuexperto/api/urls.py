from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from .blog.views import (CategoryViewSet,SubCategoryViewSet)

router = routers.DefaultRouter()
router.register('category', CategoryViewSet, basename='api_category')
router.register('subcategory', SubCategoryViewSet, basename='api_subcategory')


app_name = 'api'
urlpatterns = [

	#Token
    # path('token/', obtain_jwt_token, name='obtain_jwt_token'),
    # path('token/verify', verify_jwt_token, name='verify_jwt_token'),

    # path('buyprices', BuyPriceAverageView.as_view(), name='buyprices_list'),
    # path('btc-list/buy', BTCBuyPriceAverageView.as_view(), name='btc_prices_buy_list'),
    # path('btc-list/buy/<int:pk>', BTCBuyPriceAverageDetailView.as_view(), name='btc_prices_buy_list'),

    # path('sellprices', SellPriceAverageView.as_view(), name='sellprices_list'),
    # path('btc-list/sell', BTCSellPriceAverageView.as_view(), name='btc_prices_sell_list'),
    # path('btc-list/sell/<int:pk>', BTCSellPriceAverageDetailView.as_view(), name='btc_prices_sell_list'),


    # path('<slug:category>/subcategory/', SubCategoryList.as_view(), name='subcategory_list'),


]

urlpatterns += router.urls
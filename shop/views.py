from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework import authentication,permissions
from rest_framework.views import APIView

from shop.serializers import UserSerializer,ProductSerializer
from shop.models import Product,BasketItem,Size

# Create your views here.



class SignUpView(CreateAPIView):

    serializer_class=UserSerializer
    queryset=User.objects.all()



class ProductListView(ListAPIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    serializer_class=ProductSerializer
    queryset=Product.objects.all()



class ProductDetailView(RetrieveAPIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=ProductSerializer
    queryset=Product.objects.all() 



class AddtoCarView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):

        basket_obj=request.user.cart

        id=kwargs.get("pk")
        product_obj=Product.objects.get(id=id)

        size_name=request.data.get("size")
        size_obj=Size.objects.get(name=size_name)

        quantity=request.data.get("quantity")

        BasketItem.objects.create(
            basket_object=basket_obj,
            product_object=product_obj,
            size_object=size_obj,
            quantity=quantity

        )

        return Response(data={"message":"created"})



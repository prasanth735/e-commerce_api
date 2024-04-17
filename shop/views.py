


from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework import authentication,permissions
from rest_framework.views import APIView

from shop.serializers import UserSerializer,ProductSerializer,BasketSerializer,BasketItemSerializer
from shop.models import Product,BasketItem,Size,Order

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



class CartListView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=request.user.cart
        serializer_instance=BasketSerializer(qs)
        
        return Response(data=serializer_instance.data)
    


class CartitemUpdateView(UpdateAPIView,DestroyAPIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    serializer_class=BasketItemSerializer
    queryset=BasketItem.objects.all()

    def perform_update(self, serializer):
        
        size_name=self.request.data.get("size_object")

        size_object=Size.objects.get(name=size_name)
        serializer.save(size_object=size_object)


class CheckoutView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        
        user_obj=request.user
        delivery_address=request.data.get("delivery_address")
        phone=request.data.get("phone")
        pin=request.data.get("pin")
        email=request.data.get("email")
        payment_mode=request.data.get("payment_mode")

        order_object=Order.objects.create(
            user_object=user_obj,
            delivery_address=delivery_address,
            phone=phone,
            pin=pin,
            email=email,
            payment_mode=payment_mode
        )


        basket_items=request.user.cart.basketitems

        for bi in basket_items:
            order_object.basket_item_objects.add(bi)
            bi.is_order_placed=True
            bi.save()

        
        order_object.save()
        return Response(data={"message":"created"})

        
        




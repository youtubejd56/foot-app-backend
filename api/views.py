from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Restaurant, Order, OrderItem, Profile
from .serializers import RestaurantSerializer, OrderSerializer, ProfileSerializer, UserSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        from django.utils import timezone
        instance = self.get_object()
        # Simulate status progression based on time since creation
        diff = timezone.now() - instance.created_at
        seconds = diff.total_seconds()
        
        if seconds > 120:
            instance.status = "Delivered"
        elif seconds > 60:
            instance.status = "Out for Delivery"
        elif seconds > 30:
            instance.status = "Preparing"
        else:
            instance.status = "Order Placed"
            
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        items_data = request.data.get('items', [])
        total_price = request.data.get('total_price')
        order = Order.objects.create(items_count=len(items_data), total_price=total_price, status="Order Placed")
        for item in items_data:
            OrderItem.objects.create(order=order, restaurant_name=item.get('name', 'Unknown'), price=item.get('price', 0))
        return Response({"message": "Order placed successfully!", "order_id": order.id}, status=status.HTTP_201_CREATED)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password:
            return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

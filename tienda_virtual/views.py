from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import Order, OrderItem, Categoria
from .serializers import OrderSerializer, CategoriaSerializer

@api_view(['GET'])
def getCategories(request):
    categories = Categoria.objects.all()
    serializer = CategoriaSerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_categoria(request):
    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getProducts(request):
    products = Producto.objects.all()
    serializer = ProductoSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_producto(request):
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['PUT', 'PATCH'])
def update_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data)
    elif request.method == 'PATCH':
        serializer = ProductoSerializer(producto, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_order(request):
    if request.method == 'POST':
        order_data = request.data
        order_data['user'] = request.user.id  # Asigna el usuario actual a la orden
        order_data['status'] = Order.RECEIVED
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()

            # Agregar productos a la orden
            products = request.data.get('products', [])
            for product_data in products:
                product_id = product_data['product']
                quantity = product_data['quantity']
                size = product_data.get('size', '')
                price = product_data['price']

                product = Producto.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    size=size,
                    price=price
                )

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "La orden no existe."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
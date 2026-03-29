from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from access_controle.permissions import AccessChecker


class MockObject:
    def __init__(self, id, name, owner_id):
        self.id = id
        self.name = name
        self.owner_id = owner_id


class ProductView(APIView):
    # Моковые данные
    products = [
        MockObject(1, "Product 1", owner_id=1),
        MockObject(2, "Product 2", owner_id=2),
        MockObject(3, "Product 3", owner_id=1),
    ]

    def get(self, request, product_id=None):
        # Проверка аутентификации
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if product_id:
            # Получение одного продукта
            product = next((p for p in self.products if p.id == product_id), None)
            if not product:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            # Проверка прав
            if AccessChecker.check_permission(request.user, 'products', 'read', product):
                return Response({
                    'id': product.id,
                    'name': product.name,
                    'owner_id': product.owner_id
                })
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Получение списка продуктов
            if AccessChecker.check_permission(request.user, 'products', 'read', None):
                # Возвращаем только свои продукты
                owned_products = [p for p in self.products if p.owner_id == request.user.id]
                return Response([
                    {'id': p.id, 'name': p.name, 'owner_id': p.owner_id}
                    for p in owned_products
                ])
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if AccessChecker.check_permission(request.user, 'products', 'create'):
            new_id = max([p.id for p in self.products]) + 1 if self.products else 1
            new_product = MockObject(new_id, request.data.get('name', f"Product {new_id}"), request.user.id)
            self.products.append(new_product)
            return Response({'message': 'Product created', 'id': new_id}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, product_id):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        product = next((p for p in self.products if p.id == product_id), None)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if AccessChecker.check_permission(request.user, 'products', 'update', product):
            product.name = request.data.get('name', product.name)
            return Response({'message': 'Product updated'})

        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

# Create your views here.

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from base.models import Product, Review
from base.serializers import ProductSerializer
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def getProducts(request):
    productsTemp = Product.objects.all()
    serialized = ProductSerializer(productsTemp, many=True)
    return Response(serialized.data)


# @api_view(['GET'])
# def getTopProducts(request):


@api_view(['GET'])
def getProduct(request, pk):
    productTemp = Product.objects.get(_id=pk)
    serialized = ProductSerializer(productTemp, many=False)
    product = serialized.data

    return Response(product)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):

    user = request.user
    product = Product.objects.create(
        user=user,
        name='sample name',
        price=0,
        brand='sample brand',
        stockcount=0,
        category='sample category',
        desc=''
    )
    serialized = ProductSerializer(product, many=False)
    return Response(serialized.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):

    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.stockcount = data['stockcount']
    product.desc = data['desc']
    product.category = data['category']

    product.save()

    user = request.user

    serialized = ProductSerializer(product, many=False)
    return Response(serialized.data)


# @permission_classes([IsAdminUser])
@api_view(['POST'])
def uploadImage(request):
    data = request.data
    product_id = data['product_id']

    product = Product.objects.get(_id=product_id)
    product.image = request.FILES.get('image')
    product.save()

    return Response('Product Image Added')


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()

    return Response('Product Delete')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):

    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    alreadyExists = product.review_set.filter(user=user).exists()
    # alreadyExists = Review.user_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail': 'Product Already Reviewd'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif data['rating'] == 0:
        content = {'detail': 'Please select a Rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.email,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review Added')

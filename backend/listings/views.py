from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions
from .models import Listing
from .serializers import ListingSerializer, listingDetailSerializer
from datetime import datetime, timezone, timedelta

class ListingsView(ListAPIView):
    queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
    permission_classes = (permissions.AllowAny, )
    serializer_class = ListingSerializer
    lookup_field = 'slug'

class ListingView(RetrieveAPIView):
    queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
    serializer_class = listingDetailSerializer
    lookup_field = 'slug'

class SearchView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ListingSerializer

    def post(self, request, format=None):
        queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
        data = self.request.data

        if 'sale_type' in  data:
            queryset = queryset.filter(sale_type__iexact=data["sale_type"])

        if 'price' in  data:
            price =data['price']
            if price.endswith("+"):
               queryset = queryset.filter(price__gte=price[:-1])
            elif price.endswith("-"):
               queryset = queryset.filter(price__lte=price[:-1])
            else:
                queryset = queryset.filter(price = price)

        if 'bedrooms' in  data:    
            bedrooms =data['bedrooms']
            if bedrooms.endswith("+"):
                queryset = queryset.filter(bedrooms__gte=bedrooms[:-1])
            elif bedrooms.endswith("-"):
                queryset = queryset.filter(bedrooms__lte=bedrooms[:-1])
            else:
                queryset = queryset.filter(bedrooms = bedrooms)
       

        if 'home_type' in  data:  
            home_type = data['home_type']
            queryset = queryset.filter(home_type__iexact=home_type)

        if 'bathrooms' in  data:  
            bathrooms = data['bathrooms']
            if bathrooms == '0+':
                bathrooms = 0.0
            elif bathrooms == '1+':
                bathrooms = 1.0
            elif bathrooms == '2+':
                bathrooms = 2.0
            elif bathrooms == '3+':
                bathrooms = 3.0
            elif bathrooms == '4+':
                bathrooms = 4.0
            
            queryset = queryset.filter(bathrooms__gte=bathrooms)

        if 'sqft' in  data:  
            sqft = data['sqft']
            if sqft == '1000+':
                sqft = 1000
            elif sqft == '1200+':
                sqft = 1200
            elif sqft == '1500+':
                sqft = 1500
            elif sqft == '2000+':
                sqft = 2000
            elif sqft == 'Any':
                sqft = 0
            
            if sqft != 0:
                queryset = queryset.filter(sqft__gte=sqft)

        if ('days_listed' in  data):  
            days_passed = int(data['days_listed'])
                        
            for query in queryset:
                num_days = (datetime.now(timezone.utc) - query.list_date).days

                if days_passed != 0:
                    if num_days > days_passed:
                        slug=query.slug
                        queryset = queryset.exclude(slug__iexact=slug)
        if 'has_photos' in  data:  
            has_photos = data['has_photos']
            if has_photos == '1+':
                has_photos = 1
            elif has_photos == '3+':
                has_photos = 3
            elif has_photos == '5+':
                has_photos = 5
            elif has_photos == '10+':
                has_photos = 10
            elif has_photos == '15+':
                has_photos = 15
        
            for query in queryset:
                count = 0
                if query.photo_1:
                    count += 1
                if query.photo_2:
                    count += 1
                if query.photo_3:
                    count += 1
                if query.photo_4:
                    count += 1
                if query.photo_5:
                    count += 1
                if query.photo_6:
                    count += 1
                if query.photo_7:
                    count += 1
                if query.photo_8:
                    count += 1
                if query.photo_9:
                    count += 1
                if query.photo_main:
                    count += 1
                
                if count < has_photos:
                    slug = query.slug
                    queryset = queryset.exclude(slug__iexact=slug)
        if 'open_house' in  data:  
            open_house = data['open_house']
            queryset = queryset.filter(open_house__iexact=open_house)

        if 'keywords' in  data:  
            keywords = data['keywords']
            queryset = queryset.filter(description__icontains=keywords)

        serializer = ListingSerializer(queryset, many=True)

        return Response(serializer.data)
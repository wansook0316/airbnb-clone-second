from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django_countries import countries
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    # ccbv.co.uk 들어가서 확인하자.

    model = models.Room
    paginate_by = 10
    ordering = "created"
    page_kwarg = "page"  # page의 keyword argument를 바꿀 수 있다.
    context_object_name = "rooms"  # 이게 없으면 object_list로 남는다.


"""
    # paginator not using class based view
    from math import ceil
    from django.shortcuts import render, redirect  # render는 django에서 request에 대해 response를 만들어주는 객체다.
    from django.core.paginator import Paginator, EmptyPage
    from . import models

    # request 없이는 response가 있을 수 없다.
    # 이 때 장고에서는 render를 사용하여 이 request를 내뱉는다.
    def all_rooms(request):
        page = request.GET.get("page", 1)

        # 개신기한 부분, queryset은 호출했을 때, 바로 작동하지 않는다. (queryset is lazy)
        # 실제 필요할 때, 가져온다.. 오져부러
        room_list = models.Room.objects.all()
        paginator = Paginator(
            room_list, 10, orphans=5
        )  # orphans는 나머지 요소에 대해 전페이지에 귀속 시키는 것을 말한다.

        try:
            rooms = paginator.page(int(page))
            return render(request, "rooms/home.html", {"page": rooms})
        except EmptyPage:
            return redirect("/")

        # 이것의 return (vars)을 보면, 결과, number, paginator instance를 준다.
        # rooms = paginator.get_page(page)  # 아마 이때 queryset이 작동해서 실제 값을 불러올 것임


        
            # 수동으로 paginator 만들기
            # request는 dictionary의 자료형을 가진다.
            # request의 GET method로 받은 형식을 읽고, 그 안의 page를 key로 하는 요소를 가져와라. 없을 경우 0을 가져와라
            page = request.GET.get("page", 1)
            page = int(page or 1)
            page_size = 10
            limit = page_size * page
            offset = limit - page_size
            page_count = ceil(models.Room.objects.count() / page_size)

            # django에서는 query를 호출했을 때, 새 쿼리를 반환한다.
            all_rooms = models.Room.objects.all()[offset:limit]
            
            return render(
                request,
                "rooms/home.html",
                context={
                    "rooms": all_rooms,
                    "page": page,
                    "page_count": page_count,
                    "page_range": range(1, page_count),
                },
            )
        
"""


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


"""room_detail function based view
    def room_detail(request, pk):
        try:
            room = models.Room.objects.get(pk=pk)
            return render(request, "rooms/room_detail.html", context={"room": room})
        except models.Room.DoesNotExist:
            raise Http404()   # 이건 에러창을 뜨게 하는 것 자동으로 templates 폴더에서 404.html을 찾아서 보여준다.
            # return redirect(reverse("core:home"))   # 이건 사용자를 대상으로 한 것
"""


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")

        if country:
            # 이렇게 form에 정보를 넣어주는 것을 bounded form이라 한다. 이럴 경우 장고는 유효성 검사를 자동으로 수행한다.
            form = forms.SearchForm(request.GET)  # 이 단계에서 받은 data를 넣고, 유효성 검사까지 마쳐준다.

            if form.is_valid():  # 그 유효성 검사를 진행했을 때, 문제가 없다면
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] == room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        # 데이터 확인 과정없이 보여줘야 하는 경우가 있다.
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


"""search form manually 
    def search(request):
        city = request.GET.get("city", "Anywhere")
        city = str.capitalize(city)
        country = request.GET.get("country", "KR")
        room_type = int(request.GET.get("room_type", 0))
        price = int(request.GET.get("price", 0))
        guests = int(request.GET.get("guests", 0))
        bedrooms = int(request.GET.get("bedrooms", 0))
        beds = int(request.GET.get("beds", 0))
        baths = int(request.GET.get("baths", 0))
        instant = bool(request.GET.get("instant", False))
        superhost = bool(request.GET.get("superhost", False))
        s_amenities = request.GET.getlist("amenities")
        s_facilities = request.GET.getlist("facilities")

        form = {
            "city": city,
            "s_country": country,
            "s_room_type": room_type,
            "price": price,
            "guests": guests,
            "bedrooms": bedrooms,
            "beds": beds,
            "baths": baths,
            "s_amenities": s_amenities,
            "s_facilities": s_facilities,
            "instant": instant,
            "superhost": superhost,
        }

        room_types = models.RoomType.objects.all()
        amenities = models.Amenity.objects.all()
        facilities = models.Facility.objects.all()

        choices = {
            "countries": countries,
            "room_types": room_types,
            "amenities": amenities,
            "facilities": facilities,
        }

        filter_args = {}

        if city != "Anywhere":
            filter_args["city__startswith"] = city

        filter_args["country"] = country

        if room_type != 0:
            filter_args["room_type__pk"] == room_type

        if price != 0:
            filter_args["price__lte"] = price

        if guests != 0:
            filter_args["guests__gte"] = guests

        if bedrooms != 0:
            filter_args["bedrooms__gte"] = bedrooms

        if beds != 0:
            filter_args["beds__gte"] = beds

        if baths != 0:
            filter_args["baths__gte"] = baths

        if instant is True:
            filter_args["instant_book"] = True

        if superhost is True:
            filter_args["host__superhost"] = True

        if len(s_amenities) > 0:
            for s_amenity in s_amenities:
                filter_args["amenities__pk"] = int(s_amenity)

        if len(s_facilities) > 0:
            for s_facility in s_facilities:
                filter_args["facilities__pk"] = int(s_facility)

        rooms = models.Room.objects.filter(**filter_args)

        return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
"""

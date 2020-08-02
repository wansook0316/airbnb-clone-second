from django.utils import timezone
from django.views.generic import ListView
from . import models


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

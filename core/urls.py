from django.urls import path
from rooms import views as room_views

app_name = "core"

urlpatterns = [
    # path("", room_views.all_rooms, name="home"), # not using class based view
    path("", room_views.HomeView.as_view(), name="home"),  # 두번째 인자에는 함수만 들어갈 수 있다.
]

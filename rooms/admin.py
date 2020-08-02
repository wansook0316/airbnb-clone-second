from django.contrib import admin
from django.utils.html import (
    mark_safe,
)  # 이 부분은, 내가 output으로 내놓는 script가 안전하다고 말해주는 module이다.
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    # RoomType, Facility, Amenity, HouseRule은 모두 room을 m2m로 갖는다.
    # 그런데 위에 쓴 각각의 model에서 room에 접근하기 위해서는 모두 obj.rooms로 접근이 가능하다.
    # 따라서 이 모델들을 패널에 적용하면서 모두 같게 적용하여 보여주어도 문제가 없다.
    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()


# 현재 room에 photo를 추가하고 싶으면, photo에서 사진을 추가해주고 room을 선택해야 한다.
# 하지만 우리가 하고 싶은 것은 room에 대한 정보를 입력하는데 있어서 사진을 바로 추가하는 것이다.
# 이 방법을 가능케 하기 위해서는 room admin panel에서 photo admin panel을 불러오는 것이 좋다.
# 이렇게 하기 위한 방법을 inline admin이라 한다.


class PhotoInline(admin.TabularInline):
    model = models.Photo


# class PhotoInline(admin.StackedInline):
#     model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    inlines = (PhotoInline,)

    basicInfoFS = (
        "Basic Info",
        {"fields": ("name", "description", "country", "city", "address", "price",),},
    )
    timesFS = (
        "Times",
        {"fields": ("check_in", "check_out", "instant_book",),},
    )
    spacesFS = (
        "Spaces",
        {"fields": ("guests", "beds", "bedrooms", "baths",),},
    )
    moreFS = (
        "More About the Space",
        {
            "classes": ("collapse",),  # 화면을 접을 수 있음
            "fields": ("amenities", "facilities", "house_rules",),
        },
    )
    lastDetailFS = (
        "Last Details",
        {"fields": ("host",),},
    )

    fieldsets = (
        basicInfoFS,
        timesFS,
        spacesFS,
        moreFS,
        lastDetailFS,
    )

    # list_display에 amenity와 같은 m2m는 넣을 수 없다.
    list_display = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",  # amenities를 넣어주기 위해 몇개가 있는지 넣어준다. 이걸 사용하기위해서는 함수를 정의해야 한다.
        "count_photos",
        "total_rating",
    )

    # ordering = (
    #     "price",
    #     "price",
    #     "bedrooms",
    # )

    list_filter = (
        "host__superhost",  # 안으로 타고들어가서 필터를 먹일 수 도 있다.
        "instant_book",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )

    # model의 user가 많아졌을 때, 이것을 list로 선택하는 것이 아닌 검색을 가능하게 해준다.
    raw_id_fields = ("host",)

    # Room model에 있는 host는 FK이다.
    # 이 FK안에 있는 username을 검색 대상에 올리고 싶다면 아래와 같이 작성하자.
    search_fields = (
        "=city",
        "^host__username",
    )

    # many to many에서 작동하는 패널이다.
    # inline 필터 말고 넓직하게 보여준다.
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # 이전에 model에 있는 save method가 model을 저장함에 있어 생기는 것이라면,
    # 이것은 model에 수정하는 요청, 객체, 변화한 정보등에 대해 모두 알 수 있다.
    # 즉, 보다 섬세한 control이 가능한 부분이다.
    # def save_model(self, request, obj, form, change):
    #     print(obj, change, form)
    #     super().save_model(request, obj, form, change)

    def count_amenities(self, room):  # 두번째 인자는 model의 row를 들고 온다.
        # print(row) # 이렇게 출력해보면, 모든 room객체를 가져온다.
        # print(room.amenities.all()) # 이런 방법을 queryset이라 한다.
        return room.amenities.count()

    # 임의로 만든 column pannel에 대해 column 명을 정해줄 수 있다.
    count_amenities.short_description = "amenities"

    def count_photos(self, room):
        return room.photos.count()

    count_photos.short_description = "Photo Counts"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    # thumbnail은 개발자만 보면 된다. 실제로 사용할 일이 없어. 동영상이 아니잖아
    def get_thumbnail(self, obj):
        # return f'<img src="{obj.file.url}">'
        # 이 코드는 들어가지 않는다. 그 이유는, 이 스크립트가 실행되어 문제가 발생할 수 있기 때문이다.
        # 그렇기 때문에 장고는 이를 str화 하여 내보낸다.
        return mark_safe(f'<img src="{obj.file.url}" width="50"/>')

    get_thumbnail.short_description = "Thumbnail"

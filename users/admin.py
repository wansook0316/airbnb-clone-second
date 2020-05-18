from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# 이 부분에서 정의하는 변수들은 admin 패널의 보여짐을 수정할 수 있다.

# User model을 등록한다. 그리고 안의 내용은 CustomUserAdmin을 사용한다.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    CustomProfileFS = (
        "Custom Profile",
        {
            "fields": (
                "avatar",
                "gender",
                "bio",
                "birthdate",
                "language",
                "currency",
                "superhost",
            )
        },
    )

    defaultFieldSets = UserAdmin.fieldsets
    customFieldSets = (CustomProfileFS,)

    fieldsets = UserAdmin.fieldsets + customFieldSets


"birthdate",
"language",
"currency",
"superhost"

""" 기본 ModelAdmin을 상속받아 기능을 살펴본 코드
    @admin.register(models.User)
    class CustomUserAdmin(admin.ModelAdmin):

        Custom User Admin
        # list_display, list_filter
            # 이 친구는 row에서 보여지게 하고 싶은 변수를 정할 수 있다.
            # list_display = ("username", "email", "gender", "language", "currency", "superhost")
            # 기본적으로 보여지는 table에서 filter로 사용할 변수를 설정할 수 있다.
            # list_filter = ("language", "superhost", "currency")

        # decorator 말고 사용법
            # admin.site.register(models.User, CustomUserAdmin)
            # 이렇게 써주면 aurgument로 넣어주게 된다. 결국은 2개의 argument를 넣어주는 과정인데,
            # 위의 방법이 보다 가독성이 높기 때문에 사용된다.
            # 아래에 작성한 class가 자동적으로 augument로 들어가게 된다.
        
"""

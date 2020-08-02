# import sequence
# 1. python
# 2. 사용하는 package (django)
# 3. third-party-apps
# 4. my file

from django.db import models
from django_countries.fields import CountryField
from core import models as core_models

# from users import models as user_models

# 각 방은 장소의 형태가 있다.
# 예를 들어 전체 공간을 쓰고 싶을 수 있고, 공유하는 방을 선택하고 싶을 수 있다.
# 또는 private하게 방하나만을 쓰고 싶을 수도 있다.
# airbnb를 보면, 이런 것들이 굉장히 많다.
# 집안 규칙, 편의 시설 등
# 그래서 이러한 것들을 만들어주기 위해 일일히 모델을 추가하면 중복되는 것이 너무많다.
# 따라서 추상 클래스를 만들고 이것을 확장하는 방법으로 여러모델을 만들 것이다.


class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 그런데 Roomtype은 4가지 종류밖에 없으니까 기존에 User model에서 한방식대로
# 성별 나누는 것 처럼 하면 안되나?
# 그 방법은 약간 hard coding이라 할 수 있다.
# RoomType은 때때로 추가될 가능성이 많기 때문에 수정이 가능한 방법으로 만드는 것이 좋다.
# 아래 방법대로 한다면 admin pannel에 등록하여 수정할 수 있다.
# 하지만 기존에 User 방식은 code를 수정해야만 등록이 가능하다.
# 이런 점을 잘 판단해서 사용하는 것이 중요하다.
# 협업을 위해서도 최대한 수정을 간단하게 해주는 것이 매우 좋다.


class RoomType(AbstractItem):
    """ RoomType Model Definition """

    class Meta:
        # s가 붙는 것은 맞지만, 보여지는 방식에 있어서 수정을 하고 싶다면 아래와 같이 수정하자.
        # 아래의 예는, 시작하는 어절에 대해 대문자를 적용하고 싶어 적어주었다.
        verbose_name = "Room Type"
        # Model의 element에 대해서 정렬하여 보여줄 column을 설정할 수 있다.
        ordering = ["name"]


class Amenity(AbstractItem):
    """ Amenity Model Definition """

    class Meta:
        # 기본적으로 모델을 만들면, admin에서는 이 모델에 s를 붙여 모델에 접근할 수 있다.
        # 하지만 복수형이 s가 아닌 경우에는 보여질 때 이것을 custom화 하는 것이 옳다.
        # 그 설정을 아래와 같이 할 수 있다.
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(
        upload_to="room-photos"
    )  # upload folder에 어떤 폴더에 넣을 것인지 설정해준다.
    # 원래 Room이라고 써주는데, 이럴 경우 상하방향으로 코드를 읽기 때문에 compile시
    # Room이 무엇인지 알 수 없다.
    # 이런 경우 string으로 처리하면 알아차린다! Installed app에서 알아서 가져온다!
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)  # 필수이므로 blank 조건을 주지 않는다.
    description = models.TextField()
    country = CountryField()  # 모든 국가에 대해 넣어주는 라이브러리인 django-countries를 사용하자.
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    # Room은 User와 연관성을 가진다! 어떤? n : 1! 외래키를 사용하여 가지고 와야 한다.
    # 또한 n:1관계에서 1인 FK가 지워지면 관련된 모든 n개가 지워져야 한다. -> CASCADE
    # host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    # 아래와 같이 써주면, import할 필요도 없다. users에 있는 모델 User를 받아 먹는다.
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )  # host가 방을 찾을 때, 어떤 이름으로 접근하게 할까요?

    # 이번에는 room이 삭제된다해도 RoomType은 지워져서는 안된다.
    # 또한, 한 방은 하나의 room type을 선택하게 만들고 싶기 때문에 FK를 넣어주었다.
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )

    # many to many는 여러개를 가질 수 있으므로 변수명도 복수로 잡아준다.
    # 또한 model은 단수, 대문자를 사용하여 나타내고 변수는 소문자로 최대한 나타낸다. 띄어쓰기를 _로 잡아준다.
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    # python은 객체에 대한 이름을 설정하는 함수를 모두 가지고 있다.
    # 해당 함수는 __str__이다. 이 Room 객체가 만들어진 후에 기본 이름이 Room object로 되어 있는데,
    # 이것을 custom화 하자.
    def __str__(self):
        return self.name

    # model의 save 함수를 overriding 해서 사용한다.
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_avarage()
            return round(all_ratings / len(all_reviews))
        return 0

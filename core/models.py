from django.db import models

# 이 모델을 만드는 이유는, 다른 모델을 만드는데 있어서 반복되는 created, updated를 일일히 넣어주고 싶지 않기 때문이다.
class TimeStampedModel(models.Model):
    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)  # row(model의)를 생성할 때 시간을 기록
    updated = models.DateTimeField(auto_now=True)  # row를 저장할 때 마다 변경된 것을 기록

    # 하지만 위까지만 작성하고 migrate를 수행하면, 이것은 실제 존재하는 table로써 존재한다.
    # 그런 용도가 아니고 그냥 가져다가 쓰기 위함이기 때문에 Meta class에 추가적으로 이 class에 대한
    # 정보를 적어줄 수 있다. 이 경우에는 abstract라는 변수의 값을 True로 바꿔준다.
    # 이는, 실제로 database의 table을 만드는 것이 아니고, 추상적으로 사용할 것임을 알려준다.
    # 장고에 내제되어있는 대다수의 모델은 이 값이 true로 설정되어 있을 것이다.

    class Meta:
        abstract = True

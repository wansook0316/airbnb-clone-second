import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# 많은 삽질 후에, 완성된 모델을 적용할 때에 해야할 일
# 1. sqllite 삭제 - 다 만든 새모델을 한번에 적용하는 것이 좋다.
# 2. app의 migrations 폴더에 생성된 migrations들 다 삭제 - 같은 이유이다.
# 3. null=True를 다 지워준다.
# 4. blank=True를 넣어준다.
# 5. default 다 지워준다. -> 내가 보기에 싹다 지우고 시작하려고 하는 짓 같음

# -> migrations 는 항상 적게 유지하는 것이 좋다.
# 빈 값은 넣을 수 있게, 하지만 DB상 null은 없게. 하지만 column을 중간에 추가하는 경우에는..? 어쩔 수 없지.
# 다시 migrations, migrate, createsuperuser 해줄 것


class User(AbstractUser):

    """ Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (  # 뒤에 있는 값이 선택할 때 보여지는 값이다. 앞은 db에 저장되는 값
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    # null = DB level에서 NULL로 저장되는 것을 허용하겠니?
    # blank = 입력 단(form, application level)에서 ""을 허용하겠니?
    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(
        null=True, blank=True
    )  # 이 녀석은 빈칸이 될 수 없다. date 혹은 null만 가능하다. null은 DB단에서 빈칸을 의미
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

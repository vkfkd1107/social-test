from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from common.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, name, birthday=None, phonenumber=None, password=None):
        user = self.model(
            name=name,
            email=email,
            phonenumber=phonenumber,
            birthday=birthday,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, birthday=None, phonenumber=None, password=None):
        user = self.create_user(
            name=name,
            password=password,
            email=email,
            phonenumber=phonenumber,
            birthday=birthday,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel):
    class SingupStep(models.TextChoices):
        기본정보입력 = '기본정보입력'
        서비스이용조건미달 = '서비스이용조건미달'
        재직중 = '재직중'
        상세정보기입완료 = '상세정보기입완료'
        재직정보업데이트필요 = '재직정보업데이트필요'
        급여정보업데이트필요 = '급여정보업데이트필요'
        서비스이용조건상실 = '서비스이용조건상실'
        서비스이용불가능 = '서비스이용불가능'
        서비스일시중단 = '서비스일시중단'

    ServiceUnavailableReason = [
        ('01', '제출 기한 초과'),
        ('02', '안내된 내용과 다른 서류 제출'),
        ('03', '실물 서류 아님'),
        ('04', '서류 인식 불가'),
        ('05', '첫 이용 후 연체 상환'),
        ('06', '수신 불가능한 단말기로 확인'),
        ('07', '급여 기준 미달'),
        ('08', '재직 기준 미달'),
        ('09', '제한 업종'),
        ('10', '같은 직장 이용 가능 TO 초과'),
        ('11', '같은 직장 연체자 기준 초과'),
        ('12', '기타'),
    ]

    name = models.CharField(max_length=10, verbose_name='이름')
    phonenumber = models.CharField(
        max_length=11, verbose_name='전화번호', blank=True, null=True
    )
    email = models.EmailField(
        unique=True, blank=True
    )
    birthday = models.DateField(
        default=timezone.now, verbose_name='생년월일', null=True,
    )
    signup_status = models.CharField(
        choices=SingupStep.choices, null=True, max_length=10,
        verbose_name='가입단계'
    )
    signup_status_message = models.CharField(
        null=True, blank=True, max_length=150,
        verbose_name='가입단계 상태 메시지'
    )
    is_marketing_reception = models.BooleanField(
        default=False, verbose_name='마케팅 수신 동의 여부'
    )
    is_submit_document = models.BooleanField(
        default=False, verbose_name='서류 제출 여부'
    )
    document_url = models.URLField(null=True, blank=True, verbose_name='서류 링크')
    is_application = models.BooleanField(
        default=False, verbose_name='신청이력여부', help_text='임시필드'
    )
    health_insurance_last_updated = models.DateTimeField(
        null=True, blank=True, verbose_name='고객 건강보험 정보 마지막 업데이트 날짜'
    )
    latest_access_time = models.DateTimeField(
        null=True, blank=True, verbose_name='최근접속시간'
    )
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_temporary_password = models.BooleanField(default=False)
    service_unavailable_reason = models.CharField(
        choices=ServiceUnavailableReason, null=True, blank=True,
        max_length=100, verbose_name='서비스이용불가능 사유'
    )
    remarks = models.TextField(blank=True, default='', verbose_name='비고')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'birthday']

    class Meta:
        verbose_name_plural = '가입 정보'

    def __str__(self):
        return self.name + '_' + self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

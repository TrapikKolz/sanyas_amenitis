from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import EmailField, CharField, BooleanField, DateTimeField
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
            self, email, password=None, first_name=None, second_name=None, is_active=True, is_staff=None, is_admin=None
    ):
        if not email:
            raise ValueError("Пользователь должен иметь email")
        if not password:
            raise ValueError("Пользователь должен иметь пароль")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, second_name=second_name)
        user.password = make_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, first_name=None, second_name=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            second_name=second_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

    def create_staffuser(self, email=None, password=None, first_name=None, second_name=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            second_name=second_name,
            password=password,
            is_staff=True,
            is_admin=False
        )
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255, verbose_name='Почта')
    first_name = CharField(max_length=255, blank=True, null=True, verbose_name='Имя')
    second_name = CharField(max_length=255, blank=True, null=True, verbose_name='Фамилия')
    phone = PhoneNumberField(unique=True, null=True, verbose_name='Номер телефона')
    staff = BooleanField(default=False, verbose_name='Персонал')
    admin = BooleanField(default=False, verbose_name='Админ')
    is_active = BooleanField(default=False, verbose_name='В сети')
    timestamp = DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_short_full_name(self):
        if self.first_name and self.second_name:
            self.full_name = self.second_name + self.first_name
            return self.full_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        if not self.pk and not self.staff and not self.admin:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

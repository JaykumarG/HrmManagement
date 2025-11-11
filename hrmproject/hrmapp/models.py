from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True #this will not create Table


# =======================
# Company Model (Tenant)
# =======================
class Company(BaseModel):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)  # e.g., abc.myhrm.com
    class Meta:
        db_table = "company"
    def __str__(self):
        return self.name


# =======================
# Custom User Manager
# =======================
class UserManager(BaseUserManager):
    def create_user(self, email, company, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not company:
            raise ValueError("Company is required")

        email = self.normalize_email(email)
        user = self.model(email=email, company=company, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, company, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, company, password, **extra_fields)


# =======================
# Custom User Model
# =======================
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="users")
    full_name = models.CharField(max_length=150)
    role = models.CharField(
        max_length=20,
        choices=[
            ("ADMIN", "Admin"),
            ("MANAGER", "Manager"),
            ("EMPLOYEE", "Employee"),
        ],
        default="EMPLOYEE",
    )
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["company", "full_name"]

    objects = UserManager()

    class Meta:
        db_table = "hrm_user"

    def __str__(self):
        return f"{self.email} ({self.company.name})"
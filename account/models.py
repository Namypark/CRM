from email.policy import default
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

"""
Creating a custom model manager wehre email is the unique identifier
for authentication instead of email address
"""

"""
1.)The CustomUserManager class is defined, inheriting from Django's BaseUserManager. This allows you to customize user creation logic.

2.)create_user method: This method creates a regular user. It takes an email, password, and any extra fields as arguments. It checks if an email is provided, normalizes the email to lowercase, creates a user instance with the provided email and extra fields, sets the password using the set_password method (a built-in method for securely setting passwords), and finally saves the user instance to the database.

3.) create_superuser method: This method is used to create a superuser. It takes the same arguments as create_user along with any extra fields. It sets default values for is_staff, is_superuser, and is_active. It then checks if is_staff and is_superuser are set to True. If not, it raises ValueError with a message indicating that superusers must have those attributes set to True. Finally, it calls the create_user method with the provided arguments to create the superuser.

This CustomUserManager class is intended to be used as the manager for your custom user model in Django, allowing you to create regular users and superusers while enforcing certain rules and attribute values during creation."""


class AccountManager(BaseUserManager):
    def create_user(self, email, password, username, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(
                email
            ),  # changes capital to small letter incase you put a capital there.
            username=username,
        )
        # The set_password is an inbuilt function
        user.set_password(password)

        user.save(using=self._db)
        return user

    # creating a superuser with the create user method we created first above
    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        # can be gotten from the django admin as well
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user


"""
Import Statements:

AbstractUser is imported from django.contrib.auth.models. 
It's a base class that provides the core implementation for a user model, 
and you're going to customize it further in your Account class.

"""


class Account(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.IntegerField(null=True)
    profile_photo = models.ImageField(
        upload_to="profile_pictures", default="images/default.png"
    )
    # dates
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # perms
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]  # Email & Password are required by default.

    objects = AccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

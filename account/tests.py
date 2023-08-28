import email
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from django.urls import reverse
from django.contrib.messages import get_messages
from .forms import RegistrationForm  # Import your RegistrationForm
from .models import Account  # Import your Account model
from .views import registerUser, loginUser  # Import your registerUser view


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_valid_user(self):
        # Create a test POST data with valid user information
        post_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "phone_number": "1234567890",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        # Simulate a POST request to the registerUser view
        response = self.client.post(reverse("register"), post_data)

        # Check that the response redirects to the login page
        self.assertRedirects(response, reverse("home"))

        # Check that the user has been created
        self.assertEqual(Account.objects.count(), 1)

    def test_user_invalid_form(self):
        post_data = {
            "email": "ikengahcharlesm",
            "first_name": "Charles",
            "last_name": "Ikengah",
            "phone": "08106756090",
            "password1": "testpassword",
            "password2": "testpssword",
        }

        response = self.client.post(reverse("register"), post_data)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "register.html")
        self.assertIsInstance(response.context["form"], RegistrationForm)

    def test_register_user_get_request(self):
        # Simulate a GET request to the registerUser view
        response = self.client.get(reverse("register"))

        # Check that the response returns the registration form
        print(self.assertEqual(response.status_code, 200))
        print(self.assertTemplateUsed(response, "register.html"))
        self.assertIsInstance(response.context["form"], RegistrationForm)


class AccountManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="foo", username="foo"
        )
        self.assertEqual(
            user.email,
            "normal@user.com",
        )
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superadmin)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNotNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo", username="")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo", username="park"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superadmin)
        # try:
        #     # username is None for the AbstractUser option
        #     # username does not exist for the AbstractBaseUser option
        #     self.assertIsNotNone(admin_user.username)
        # except AttributeError:
        #     pass
        # with self.assertRaises(ValueError()):
        #     try:
        #         user = User.objects.create_superuser(
        #             email="super1@user.com",
        #             password="foo",
        #             username="p",
        #             is_active=False,
        #         )
        #     except ValueError as e:
        #         print(f"Caught exception: {e}")
        #         raise e  # Re-raise the exception for the test to catch

        # Ensure that the user creation and exception handling were attempted

from django.contrib.auth.models import User, UserManager
from django.test import Client, TestCase
from django.urls import reverse

from geraete.models import Company, Device, DeviceCat, Employee, SiteUser


class Setup(TestCase):
    fixtures = ["all.json"]

    def setUp(self):
        self.user = User.objects.create_user("user", password="user")
        self.siteuser = SiteUser.objects.create(user=self.user, company_id=1)


class LoggedInSetup(Setup):
    def setUp(self):
        super().setUp()
        self.client.login(username="user", password="user")


PROTECTED_URLS = (
    "employees",
    "prof_groups",
    "prof_group_add",
    # "get_devices",
    "lacking",
)


class Views_Get_Test(Setup):
    def test_get(self):
        for name in PROTECTED_URLS:
            response = self.client.get(reverse(name))
            assert response.status_code == 302


class Views_LoggedIn_Get_Test(LoggedInSetup):
    def test_get(self):
        for name in PROTECTED_URLS:
            response = self.client.get(reverse(name))
            assert response.status_code == 200


class GetDevices(LoggedInSetup):
    def test_post(self):
        response = self.client.post(
            reverse("get_devices"), {"instructor": "1"}
        )
        assert response.status_code == 200
        self.assertTemplateUsed(
            response, "geraete/partials/instructor_devices.html"
        )
        devices = response.context["devices"]
        assert len(devices) == 1
        assert devices[0].id == 1
        print(response.content)

    def test_post_invalid(self):
        response = self.client.post(
            reverse("get_devices"), {"instructor": "100"}
        )
        assert response.status_code == 200
        devices = response.context["devices"]
        assert len(devices) == 0


class PrimaryInstruction(LoggedInSetup):
    def test_primaryinstruction(self):
        devices = Device.get_for_instructor(1, 1)
        assert len(devices) == 1
        assert devices[0].id == 1
        response = self.client.post(
            reverse("primaryinstruction"),
            {
                "day": "06.03.2022",
                "instructor": "Hr. Atmos",
                "device_company": "Atmos",
                "instructed": ["1"],
                "devices": ["2"],
            },
        )
        devices = Device.get_for_instructor(1, 1)
        assert len(devices) == 2
        assert set([d.id for d in devices]) == set([1, 2])


# class ProfGroup_Views_Test(LoggedInSetup):
#     def test_add_user_view(self):
#         response = self.client.get("include url for add user view")
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(
#             response, "include template name to render the response"
#         )

#     # Invalid Data
#     def test_add_user_invalidform_view(self):
#         response = self.client.post(
#             "include url to post the data given",
#             {
#                 "email": "admin@mp.com",
#                 "password": "",
#                 "first_name": "mp",
#                 "phone": 12345678,
#             },
#         )
#         self.assertTrue('"error": true' in response.content)

#     # Valid Data
#     def test_add_admin_form_view(self):
#         user_count = User.objects.count()
#         response = self.client.post(
#             "include url to post the data given",
#             {"email": "user@mp.com", "password": "user", "first_name": "user"},
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(User.objects.count(), user_count + 1)
#         self.assertTrue('"error": false' in response.content)

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertTemplateNotUsed
from nutrition.models import Plate


@pytest.mark.django_db
def test_plates_list_requires_authentication(client: Client):
    """
    Given an unauthenticated user
    When try to access the plates list
    Then should be redirected to the login page
    """
    response = client.get(reverse("nutrition:user_plates"))
    print(response)
    assert response.status_code == 302
    assert "login" in response.url


# test user sees only his plates
@pytest.mark.django_db
def test_plates_user_sees_only_own_plates(client, user1, user2, plates_user1, plates_user2):
    """
    Given 2 users with 2 plates each
    When user1 access his plates list
    Then should see only his plates and not the plates of user2
    """
    client.force_login(user1)
    response = client.get(reverse("nutrition:user_plates"))
    plates = response.context["plates"]
    assert all(plate in plates for plate in plates_user1) # user1 see only his plates
    assert all(plate not in plates for plate in plates_user2) # user1 don't see plates of user2


# test url/search bar in a plates list with "poulet" in the key name
@pytest.mark.django_db
def test_plates_list_search(client, user1):
    plate_melon = Plate.objects.create(name="Melon", user=user1)
    plate_poulet = Plate.objects.create(name="Poulet", user=user1)
    client.force_login(user1)
    response = client.get(reverse("nutrition:user_plates"), {"search": "poulet"})
    plates = response.context["plates"]
    assert plate_poulet in plates
    assert plate_melon not in plates


# test "nutrition/user_plates.html" template with url hardcoding, use specific asserts
@pytest.mark.django_db
def test_plates_list_template(client, user1):
    client.force_login(user1)
    response = client.get(reverse("nutrition:user_plates"))
    print(response)
    assert response.status_code == 200 # 200 = OK
    assertTemplateUsed(response, "nutrition/user_plates.html") # template used


# control if htmx request is used
@pytest.mark.django_db
def test_plates_list_htmx_template(client, user1):
    client.force_login(user1)
    response = client.get(reverse("nutrition:user_plates"), HTTP_HX_REQUEST="true") # HTTP_HX_REQUEST = htmx request
    print(response)
    assert response.status_code == 200 # 200 = OK
    assertTemplateUsed(response, "nutrition/partials/plates_list.html") # partial template used
    assertTemplateNotUsed(response, "nutrition/user_plates.html") # the main template not used

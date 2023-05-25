from django.urls import reverse

from conftest import _test_not_logged_user
from ducks.models import Duck, DuckRate


def test_add_duck_get(client, db, user):
    url = reverse('ducks:add')
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == 200
    assert '<h2 class="border-bottom border-top border-black p-2">Add Duck</h2>' in response.content.decode('utf-8')


def test_add_duck_post(client, db, user, image):
    url = reverse('ducks:add')
    client.force_login(user)
    data = {
        'name': 'test duck',
        'description': 'test duck description',
        'image': image,
        'avg_weight': 3.2,
        'strength': 5.4,
        'intelligence': 5.4,
        'agility': 5.4,
        'charisma': 5.4,
    }
    duck_counter = Duck.objects.count()

    redirect = client.post(url, data)
    duck_counted_after = Duck.objects.count()
    added_duck = Duck.objects.first()
    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert duck_counter == duck_counted_after - 1
    assert added_duck.name == data['name']


def test_duck_details(client, db, duck):
    url = reverse('ducks:details', kwargs={'pk': duck.pk})

    response = client.get(url)

    assert response.status_code == 200
    assert '<h3 class="p-2 border-bottom border-black">Test Duck</h3>' in response.content.decode('utf-8')


def test_rate_duck(client, db, duck, user):
    url = reverse('ducks:rate', kwargs={'pk': duck.pk})
    client.force_login(user)
    data = {
        'rate': 10,
    }
    num_of_rates = DuckRate.objects.filter(duck=duck).count()

    redirect = client.post(url, data)
    num_of_rates_after = DuckRate.objects.filter(duck=duck).count()

    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert num_of_rates == num_of_rates_after - 1


def test_add_duck_no_permission(client, db):
    redirect, response = _test_not_logged_user(client, reverse('ducks:add'))

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert '<h2 class="border-bottom border-top border-black p-2">Login</h2>' in response.content.decode('utf-8')


def test_rate_duck_no_permission(client, db, duck):
    redirect, response = _test_not_logged_user(client, reverse('ducks:rate', kwargs={'pk': duck.pk}))

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert '<h2 class="border-bottom border-top border-black p-2">Login</h2>' in response.content.decode('utf-8')

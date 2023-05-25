from django.urls import reverse

from ducks.models import Duck


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


def test_add_fav_duck(client, db, duck, user):
    url = reverse('users:add-fav-duck', kwargs={'pk': duck.pk})
    client.force_login(user)
    fav_ducks_num = user.fav_ducks.count()

    redirect = client.get(url)
    fav_ducks_num_after = user.fav_ducks.count()
    fav_duck = user.fav_ducks.first()

    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert fav_ducks_num == fav_ducks_num_after - 1
    assert fav_duck.name == duck.name


def test_delete_fav_duck(client, db, user, duck):
    user.fav_ducks.add(duck)
    url = reverse('users:del-fav-duck', kwargs={'pk': duck.pk})
    client.force_login(user)
    fav_ducks_num = user.fav_ducks.count()

    redirect = client.get(url)
    fav_ducks_num_after = user.fav_ducks.count()

    response = client.get(redirect.url)

    assert response.status_code == 200
    assert redirect.status_code == 302
    assert fav_ducks_num == fav_ducks_num_after + 1
    
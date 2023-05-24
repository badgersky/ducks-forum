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

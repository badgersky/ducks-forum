from django.urls import reverse


def test_add_duck_get(client, db, user):
    url = reverse('ducks:add')
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == 200
    assert '<h2 class="border-bottom border-top border-black p-2">Add Duck</h2>' in response.content.decode('utf-8')
    
from django.urls import reverse


def test_registration_get(db, client):
    url = reverse('users:register')

    response = client.get(url)

    assert response.status_code == 200
    assert '<h2 class="border-bottom border-top border-black p-2">Register</h2>' in response.content.decode('utf-8')


def test_login_get(db, client):
    url = reverse('users:login')

    response = client.get(url)

    assert response.status_code == 200
    assert '<h2 class="border-bottom border-top border-black p-2">Login</h2>' in response.content.decode('utf-8')

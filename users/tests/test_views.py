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


def test_registration_post(db, django_user_model, client):
    url = reverse('users:register')
    data = {
        'username': 'username1',
        'password': 'password1',
        'confirm_password': 'password1',
        }

    redirect = client.post(url, data)
    user = django_user_model.objects.get(username=data['username'])

    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert user.username == data['username']
    assert response.status_code == 200
    assert 'Registration Successful, please login' in response.content.decode('utf-8')


def test_login_post(user, db, client):
    url = reverse('users:login')
    data = {
        'username': 'username1',
        'password': 'password1',
        }

    redirect = client.post(url, data)

    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert '<h2 class="border-bottom border-top border-black p-2">Most popular threads</h2>' in \
           response.content.decode('utf-8')

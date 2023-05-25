from django.urls import reverse

from conftest import _test_not_logged_user


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
    assert f'<span class="navbar-text m-2">Logged in {data["username"]}</span>' in response.content.decode('utf-8')


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


def test_add_fav_duck_no_permission(client, db, duck):
    redirect, response = _test_not_logged_user(client, reverse('users:add-fav-duck', kwargs={'pk': duck.pk}))

    assert '<h2 class="border-bottom border-top border-black p-2">Login</h2>' in response.content.decode('utf-8')

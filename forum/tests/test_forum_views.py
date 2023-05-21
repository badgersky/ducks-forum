from django.urls import reverse

from forum.models import Thread


def test_create_thread_get(client, db, user):
    url = reverse('forum:create')
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == 200
    assert '<h2 class="border-bottom border-top border-black p-2">Start Thread</h2>' in response.content.decode('utf-8')


def test_create_thread_post(client, db, user):
    url = reverse('forum:create')
    data = {
        'subject': 'subject1',
        'content': 'content1',
    }
    client.force_login(user)
    thread_counter = Thread.objects.count()

    redirect = client.post(url, data)
    thread = Thread.objects.get(creator=user)
    thread_counter_after = Thread.objects.count()

    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert thread.content == data['content']
    assert thread_counter == thread_counter_after - 1

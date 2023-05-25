from django.urls import reverse

from conftest import _test_not_logged_user
from forum.models import Thread, Comment, LikeThread, LikeComment


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


def test_add_comment(client, db, thread, user):
    url = reverse('forum:add-comment', kwargs={'pk': thread.pk})
    data = {
        'content': 'comment content',
    }
    client.force_login(user)
    comments_counter = Comment.objects.count()

    redirect = client.post(url, data)
    comment = Comment.objects.get(user=user, thread=thread)
    comments_counter_after = Comment.objects.count()

    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert comment.content == data['content']
    assert comments_counter == comments_counter_after - 1


def test_like_thread(client, db, user, thread):
    url = reverse('forum:like-thread', kwargs={'pk': thread.pk})
    client.force_login(user)
    likes_before = LikeThread.objects.filter(thread=thread).count()

    redirect = client.get(url)
    likes_after = LikeThread.objects.filter(thread=thread).count()
    response = client.get(redirect.url)

    assert likes_before == likes_after - 1
    assert redirect.status_code == 302
    assert response.status_code == 200


def test_like_comment(client, db, user, thread, comment):
    url = reverse('forum:like-comment', kwargs={'thr_pk': thread.pk, 'com_pk': comment.pk})
    client.force_login(user)
    likes_before = LikeComment.objects.filter(comment=comment, user=user).count()

    redirect = client.get(url)
    likes_after = LikeComment.objects.filter(comment=comment, user=user).count()
    response = client.get(redirect.url)

    assert likes_before == likes_after - 1
    assert redirect.status_code == 302
    assert response.status_code == 200


def test_like_comment_no_permission(client, db, thread, comment):
    url = reverse('forum:like-comment', kwargs={'thr_pk': thread.pk, 'com_pk': comment.pk})
    likes_before = LikeComment.objects.filter(comment=comment).count()

    redirect, response = _test_not_logged_user(client, url)
    likes_after = LikeComment.objects.filter(comment=comment).count()

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert likes_before == likes_after
    assert '<h2 class="border-bottom border-top border-black p-2">Login</h2>' in response.content.decode('utf-8')


def test_like_thread_no_permission(client, db, thread):
    url = reverse('forum:like-thread', kwargs={'pk': thread.pk})
    likes_before = LikeThread.objects.filter(thread=thread).count()

    redirect, response = _test_not_logged_user(client, url)
    likes_after = LikeThread.objects.filter(thread=thread).count()

    assert response.status_code == 200
    assert redirect.status_code == 302
    assert likes_before == likes_after
    assert '<h2 class="border-bottom border-top border-black p-2">Login</h2>' in response.content.decode('utf-8')


def test_add_comment_no_permission(client, db, thread):
    url = reverse('forum:add-comment', kwargs={'pk': thread.pk})
    comments_num = Comment.objects.filter(thread=thread).count()

    redirect, response = _test_not_logged_user(client, url)
    comments_num_after = Comment.objects.filter(thread=thread).count()

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert comments_num == comments_num_after
    assert '<h2 class="border-bottom border-top border-black p-2">Login</h2>' in response.content.decode('utf-8')

from django.test import TestCase
from django.urls import reverse

from blog.models import Blog
from users.models import User


class BlogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone_number="+123456789",
            is_staff=True,
            is_active=True,
            is_superuser=True,
            password="Admin"
        )

        self.blog = Blog.objects.create(title="blog 1", content="testing",
                                        is_premium=True, count_view=2)

    def test_get_create_blog(self):
        new_blog = Blog.objects.create(title="test", content="test1",
                                       is_premium=True, count_view=1)

        self.assertEqual(new_blog.title, 'test')
        self.assertEqual(new_blog.content, 'test1')

    def test_get_list_blog(self):
        url = reverse("blog:blog_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_update_blog(self):
        self.blog.title = 'Lux'
        self.blog.content = 'Good boy'
        self.blog.save()
        self.assertEqual(self.blog.title, 'Lux')
        self.assertNotEqual(self.blog.content, 'testing')

    def test_get_delete_blog(self):
        self.blog.delete()
        self.assertEqual(Blog.objects.count(), 0)

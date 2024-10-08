from django.test import TestCase, Client
from django.urls import reverse
from main_app.models import Contact, TeamMember, GalleryItem
from io import BytesIO
import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile


# View Tests
class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/index.html')


class AboutViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/about.html')


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/contact.html')

    def test_contact_view_post(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'mobile': '1234567890',
            'subject': 'Inquiry',
            'message': 'I would like to know more about your services.',
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.first().name, 'John Doe')


class CoursesViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_courses_view(self):
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/courses.html')


class CourseDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_course_detail_view(self):
        response = self.client.get(reverse('course-detail'))  # Correct URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/course-detail.html')


class OurTeamViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_our_team_view(self):
        response = self.client.get(reverse('our-team'))  # Correct URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/our-team.html')

class GalleryImagesViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_gallery_images_view(self):
        response = self.client.get(reverse('gallery_images'))  # Correct URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/gallery_images.html')


class GalleryVideosViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_gallery_videos_view(self):
        response = self.client.get(reverse('gallery_videos'))  # Correct URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/gallery_videos.html')


class FooterGalleryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create 6 valid image items with a file
        for i in range(6):
            GalleryItem.objects.create(title=f'Image {i}', media_type='image', file='gallery/sample_image.jpg')

    def test_footer_gallery_context(self):
        response = self.client.get(reverse('index'))  # Correct URL name
        context = response.context['gallery_items']
        self.assertEqual(len(context), 6)  # Only 6 images should be shown
        self.assertEqual(context[0].title, 'Image 5')  # The latest image is first



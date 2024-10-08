from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main_app.models import Contact, TeamMember, GalleryItem
from django.utils import timezone
from io import BytesIO
import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

# Model Tests
class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='John Doe',
            email='john@example.com',
            mobile_no='1234567890',
            subject='Inquiry',
            message='Test message'
        )

    def test_contact_creation(self):
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(str(self.contact), 'John Doe - john@example.com')


class TeamMemberModelTest(TestCase):
    def setUp(self):
        self.member = TeamMember.objects.create(
            name='Jane Smith',
            designation='Manager',
            facebook_url='http://facebook.com',
            twitter_url='http://twitter.com',
            instagram_url='http://instagram.com'
        )

    def test_team_member_creation(self):
        self.assertEqual(TeamMember.objects.count(), 1)
        self.assertEqual(str(self.member), 'Jane Smith')


class GalleryItemModelTest(TestCase):
    def setUp(self):
        self.gallery_item = GalleryItem.objects.create(
            title='Sample Image',
            media_type='image',
            file='gallery/sample_image.jpg'
        )

    def test_gallery_item_creation(self):
        self.assertEqual(GalleryItem.objects.count(), 1)
        self.assertEqual(str(self.gallery_item), 'Sample Image')

    def test_gallery_item_clean_image(self):
        with self.assertRaises(Exception):
            gallery_item = GalleryItem.objects.create(
                title='Sample Video',
                media_type='image',
                video_url='http://video.com/sample.mp4'
            )
            gallery_item.clean()


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
        response = self.client.get(reverse('course_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/course-detail.html')


class OurTeamViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        TeamMember.objects.create(name='Jane Smith', designation='Manager')

    def test_our_team_view(self):
        response = self.client.get(reverse('our_team'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/our-team.html')
        self.assertEqual(len(response.context['team_members']), 1)
        self.assertEqual(response.context['team_members'][0].name, 'Jane Smith')


class GalleryImagesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        GalleryItem.objects.create(title='Beautiful Sunset', media_type='image')

    def test_gallery_images_view(self):
        response = self.client.get(reverse('gallery_images_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/gallery_images.html')
        self.assertEqual(len(response.context['gallery_items']), 1)
        self.assertEqual(response.context['gallery_items'][0].title, 'Beautiful Sunset')


class GalleryVideosViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        GalleryItem.objects.create(title='Inspiring Video', media_type='video')

    def test_gallery_videos_view(self):
        response = self.client.get(reverse('gallery_videos_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app_templates/gallery_videos.html')
        self.assertEqual(len(response.context['gallery_items']), 1)
        self.assertEqual(response.context['gallery_items'][0].title, 'Inspiring Video')


class FooterGalleryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        for i in range(7):
            GalleryItem.objects.create(title=f'Image {i}', media_type='image')

    def test_footer_gallery_context(self):
        response = self.client.get(reverse('index'))  # Assuming 'footer_gallery' context is used on index page
        context = response.context['gallery_items']
        self.assertEqual(len(context), 6)
        self.assertEqual(context[0].title, 'Image 6')  # Latest image first

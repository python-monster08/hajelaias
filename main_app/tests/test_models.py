from django.test import TestCase
from main_app.models import Contact, TeamMember, GalleryItem
from django.core.exceptions import ValidationError


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
        with self.assertRaises(ValidationError):
            gallery_item = GalleryItem.objects.create(
                title='Sample Video',
                media_type='image',
                video_url='http://video.com/sample.mp4'
            )
            gallery_item.clean()

    def test_gallery_item_clean_video(self):
        with self.assertRaises(ValidationError):
            gallery_item = GalleryItem.objects.create(
                title='Sample Image',
                media_type='video',
                file='gallery/sample_image.jpg'
            )
            gallery_item.clean()

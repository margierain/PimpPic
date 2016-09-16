from PIL import Image
from django.contrib.auth.models import User
from pic. models import *
from django.test import TestCase, override_settings
from faker import Factory
import tempfile
fake = Factory.create()

def get_dummy_image(temp_file):
    """Generate dummy image file."""

    color = (255, 0, 0, 0)
    size = (250, 250)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file

class PhotoEditingTest(TestCase):
    """Test model creation ."""

    def setUp(self):
        """Set up user dummy data."""

        user = User.objects.create(
            username=fake.name().replace(' ', ''), password=fake.password())
        self.uploader = User.objects.filter(id=user.id).first()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_image_upload(self):
        """Check correct image upload and filters creation."""

        image_uploded = tempfile.NamedTemporaryFile(suffix=".jpg").name
        test_image = get_temporary_image(image_uploded)
        picture = models.Image.objects.create(
            image=test_image, uploader=self.uploader)
        search = models.Image.objects.filter(image=test_image).first()
        self.assertEqual(len(models.Image.objects.all()), 1)
        self.assertEqual(len(models.Img_edited.objects.all()), 10)
        self.assertTrue(models.Img_edited.objects.get(effect='blur'))
        self.assertIn(test_image, search.original_image.name)
        self.assertIsInstance(picture, models.Image)
import tempfile
from PIL import Image
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from django.test import override_settings
from pic.models import Photo, Folder


def get_dummy_image(temp_file):
    """Generate dummy image file."""

    color = (255, 0, 0, 0)
    size = (250, 250)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file

class PhotoEditingTest(APITestCase):
    """Test model creation ."""

    def setUp(self):
        """Set up user dummy data."""
        data = {
        "name":"maggie", "password":"567898ggdh"
        }
        user = User.objects.create(
            username=data["name"], password=data["password"])
        self.uploader = User.objects.filter(id=user.id).first()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_image_upload(self):
        """Check correct image upload and filters creation."""
        self.client.force_authenticate(self.uploader)
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        test_image = get_dummy_image(image)
        picture = Photo.objects.create(
            image=test_image, uploader=self.uploader)
        picture.save()
        search = Photo.objects.filter(image=test_image).first()
        self.assertEqual(len(Photo.objects.all()), 1)
        self.assertIn(test_image, str(search.image))
        self.assertIsInstance(picture, Photo)

    def test_folder_model(self):
        """Test folder model"""
        folder = Folder.objects.create(name="new_test_folder", creator=self.uploader)
        folder.save()
        self.assertEqual(len(Folder.objects.all()), 1)
        self.assertIn("new_test_folder", str(folder.name))
        self.assertIsInstance(folder, Folder)

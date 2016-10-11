from rest_framework.test import APITestCase
from rest_framework import status
from selenium import webdriver
import os
import json
from pic.models import Photo, Folder

# Facebook graphapi test user access token
access_token = 'EAACEdEose0cBAAoO8BU1w58FzkZAHBlcgItTQdPu9OSVDmSrdaZAMQRFSZBQUbpiroFAVKFJYjOgp6PWDcU0jjq5HnfP9T3m6uBn2QZAVqxhZAgII9gE0oMmBSocXDObeJi2ygQbBwFSxyIqlbUudn2q4ElYCEPLuWPgg9ZAhWQAZDZD'


class ImageAPITest(APITestCase):

    def setUp(self):
        """Create test user and test images"""
        self.client.get("/api/register/facebook/?access_token=" + access_token)
        Folder.objects.create(name="Adventure")
        Photo.objects.create(image="images/adventure.png",
                            edited_image = "images/adventure.png",
                            folder = null,
                             date_created="2016-08-03 11:12:12.959349+03",
                             date_modified="2016-08-03 11:12:12.95939+03",
                             category=1, uploader_id=1)
        Photo.objects.create(image="images/fashion.png",
                            edited_image = "images/adventure.png",
                            folder = 1,
                             date_created="2016-08-03 11:12:12.959349+03",
                             date_modified="2016 - 08 - 03 11: 12: 12.95939 + 03",
                             uploader_id=1)

def create_folder(client, name):
        """Set up folder to store test images"""
        data = {
            'name': name
        }
        return client.post('/api/folders/', data)


class FolderTest(APITestCase):
    """Test /api/v1/folders/ endpoint"""

    def setUp(self):
        """Set up fb login."""
       self.client = self.client.get("/api/register/facebook/?access_token=" + access_token)

    def test_folder_create(self):
        response = create_folder(self.client, 'test')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_folder_update(self):
        response = create_folder(self.client, 'test')
        result = decode_json(response)
        folder_id = result.get('id', 0)
        response = self.client.put('/api/folders/' + str(folder_id) + '/', {'name':"test edit"})
        result = decode_json(response)
        self.assertEqual(result.get('name'), 'test edit')

    def test_folder_delete(self):
        response = create_folder(self.client, 'test')
        result = decode_json(response)
        folder_id = result.get('id', 0)
        response = self.client.delete('/api/folders/' + str(folder_id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_folder_display(self):
        create_folder(self.client, 'test')
        create_folder(self.client, 'test 2')
        response = self.client.get('/api/folders/')
        result = decode_json(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count'), 2)


class ImageTest(APITestCase):
    """Test /api/pics/ endpoint """

    def setUp(self):
        """Set up base user and details for test running."""
        self.client = self.client.get("/api/register/facebook/?access_token=" + access_token)


    def upload_photo(client, folder_id=0):
        """Upload image set up"""
        path = os.path.join(os.path.dirname(os.path.dirname(
            os.path.dirname(__file__))), 'static/images/imageFolder.jpeg')
        with open(path) as image:
            data = {
                'image': image,
                'folder_id': folder_id
            }
            return client.post('/api/photos/', data)
        return None

    def decode_json(response):
        return json.loads(response.content)


    def photo_effect(self, effects):
        response = self.upload_photo(self.client)
        result = self.decode_json(response)
        img_id = result.get('id', 0)
        data = {
            'img_id': photo_id,
            'effects': effects
        }
        response = self.client.post(
            '/api/photos/' + str(img_id) + '/preview/', data)
        return self.decode_json(response)

    def test_img_update(self):
        """ Test images can be updated"""
        response = self.upload_photo(self.client)
        result = self.decode_json(response)
        img_id = result.get('id', 0)
        response = self.client.put(
            '/api/photos/' + str(img_id) + '/', {'title': 'test image'})
        result = self.decode_json(response)
        self.assertEqual(result.get('id'), img_id)
        self.assertEqual(result.get('title'), 'test image')

    def test__downloading_image(self):
        """ Test user can download images they have edited"""
        response = self.upload_photo(self.client)
        result = self.decode_json(response)
        img_id = result.get('id', 0)
        response = self.client.get('/download?image=' + str(img_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_img_deletion(self):
        """ Test use can delete images """
        response = self.upload_photo(self.client)
        result = self.decode_json(response)
        img_id = result.get('id', 0)
        response = self.client.delete('/api/photos/' + str(img_id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_display_of_images(self):
        """ Test all images are displayed on get request"""
        self.upload_photo(self.client)
        response = self.client.get('/api/photos/')
        result = self.decode_json(response)
        self.assertEqual(result.get('count'), 1)

    def test_folder_list_photos(self):
        """Test user can view folder per folder"""
        response = create_folder(self.client, 'test')
        result = self.decode_json(response)
        folder_id = result.get('id', 0)
        self.upload_photo(self.client, folder_id)
        response = self.client.get(
            '/api/folders/' + str(folder_id) + '/photos/')
        result = self.decode_json(response)
        self.assertEqual(result.get('count'), 1)

    def test_folder_list_untitled_photos(self):
        """ Test that an untitled folder can contain images"""
        self.upload_photo(self.client)
        self.upload_photo(self.client)
        response = self.client.get('/api/folders/0/photos/')
        result = self.decode_json(response)
        self.assertEqual(result.get('count'), 1)

    def test_photo_effect_update(self):
        """ Test user can update effects on images"""
        response = self.upload_photo(self.client)
        result = self.decode_json(response)
        img_id = result.get('id', 0)
        data = {
            'title': 'update img effect',
            'effects': '{"enhance":{"Brightness":"65"},"filter":{"blur":"true"},"transform":{"mirror":"true"},"effect":{"quantize":"50","gaussian_blur":"50","auto_contrast":"50","posterize":"50","unsharp_mask":"50","solarize":"50","remove_border":"50","rotate":"50"}}'
        }
        response = self.client.put('/api/photos/' + str(img_id) + '/', data)
        result = self.decode_json(response)
        self.assertEqual(result.get('title'), 'update img effect')

    def test_photo_effect_preview(self):
        """ Test user can preview efects to be applied on images"""
        response = self.upload_photo(self.client)
        result = self.photo_effect(
            '{"transform":{"vertical_flip":"true","invert":"true","grayscale":"true","black_and_white":"true","equalize":"true"}}')
        applied_effect = 'invert' in result.get('applied_effects', [])
        self.assertNotEqual(result.get('image'), None)
        self.assertTrue(applied_effect)

    def test_text_overlay_on_images(self):
        """ Test user can append text on images"""
        response = self.upload_photo(self.client)
        result = self.photo_effect(
            '{"text_overlay":{"textValue":"love is key","fontSize":"26","x":"22","y":"24","color":"#ff3400","font_name":"dahot2.Filxgirl.ttf"}}')
        applied_effect = 'text' in result.get('applied_effects', [])
        self.assertTrue(applied_effect)
        self.assertNotEqual(result.get('image'), '')
        self.assertNotEqual(result.get('image'), None)

    def test_photo_effect_colorize(self):
        """ Test user can colorize images"""
        response = self.upload_photo(self.client)
        result = self.photo_effect(
            '{"colorize":{"black":"#5f1212","white":"#8b572a"}}')
        applied_effect = 'colorize' in result.get('applied_effects', [])
        self.assertTrue(applied_effect)
        self.assertNotEqual(result.get('image'), '')
        self.assertNotEqual(result.get('image'), None)

    def test_photo_effect_border(self):
        """ Test user can apply border effect"""
        response = self.upload_photo(self.client)
        result = self.photo_effect(
            '{"border":{"size":"26","border_color":"#ff3737"}}')
        applied_effect = 'border' in result.get('applied_effects', [])
        self.assertTrue(applied_effect)
        self.assertNotEqual(result.get('image'), '')
        self.assertNotEqual(result.get('image'), None)

    def test_photo_share(self):
        """ Test user can share photoes"""
        response = self.upload_photo(self.client)
        result = self.decode_json(response)
        share_id = result.get('share_code', '')
        response = self.client.get('/api/photos/share/?share_id=' + share_id)
        result = self.decode_json(response)
        self.assertEqual(result.get('share_code'), share_id)

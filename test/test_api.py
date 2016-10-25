from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status
import os
import json
from pic.models import Photo, Folder
from PIL import Image
import tempfile
from django.test import override_settings
from django.core.urlresolvers import reverse

# Facebook graphapi test user access token
fb_token = ''
class FolderTest(APITestCase):
    """Test /api/folders/ endpoint"""


    def setUp(self):
        """Set up fb login."""
        self.client.get("/login/facebook/" + "Bearer facebook " + fb_token)
        user = User.objects.create(
            username='testuser', password='testpassword')
        self.uploader = User.objects.filter(id=user.id).first()
        data = {
            'name': 'test_folder'
        }
        create_folder = Folder.objects.create(name="test_folder", creator=self.uploader)
       
        
    def test_get_all_images(self):
        """Test for getting all the images"""
        self.client.credentials(
             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        response = self.client.get('/api/folders/')
        self.assertEqual(response.status_code, 200)
    

    def test_unauthorized_access_to_folders_is_not_allowed(self):
        """Test that a user cannot access API without credentials."""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + 'auth_token')
        response = self.client.get('/api/folders/')
        self.assertEqual(response.status_code, 403)
        detail = response.data.get('detail')
        self.assertIn('Invalid OAuth access token', detail)

        
    def test_folder_create(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        data = {
            'name': 'test_folder'
        }
        response = self.client.post('/api/folders/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_access_to_images_is_not_allowed(self):
        """Test that a user cannot access API without credentials."""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + 'auth_token')
        response = self.client.get('/api/images/')
        self.assertEqual(response.status_code, 403)
        detail = response.data.get('detail')
        self.assertIn('Invalid OAuth access token', detail)
    
    # def test_folder_update(self):
    #     """Test folder name update"""
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
    #     folder = Folder.objects.first()
    #     url = "/api/folder/{}/".format(folder.id)
    #     folder_name = {
    #         'name': 'test_folder'
    #     }
    #     response = self.client.put(url, folder_name, format='json')
    #     print('jill', folder_name, 'hill', folder_name['name'] )
    #     self.assertIn(folder_name['name'], response.folder_name.get('name'))
       
        

    # def test_folder_delete(self):
    #     response = create_folder(self.client, 'test')
    #     result = decode_json(response)
    #     folder_id = result.get('id', 0)
    #     response = self.client.delete('/api/folders/' + str(folder_id) + '/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
def get_temporary_image(temp_file):
    """Generate dummy image file."""
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(temp_file, 'jpeg')
    return temp_file


class ImageTest(APITestCase):
    """Test /api/pics/ endpoint """

    def setUp(self):
        """Set up base user and details for test running."""
        self.client = self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)


    # def upload_photo(client, folder_id=0):
    #     """Upload image set up"""
    #     path = os.path.join(os.path.dirname(os.path.dirname(
    #         os.path.dirname(__file__))), 'media/images/imageFolder.jpeg')
    #     with open(path) as image:
    #         data = {
    #             'image': image,
    #             'folder_id': folder_id
    #         }
    #         return client.post('/api/photos/', data)
    #     return None

    # def decode_json(response):
    #     return json.loads(response.content)


    # def photo_effect(self, effects):
    #     response = self.upload_photo(self.client)
    #     result = self.decode_json(response)
    #     img_id = result.get('id', 0)
    #     data = {
    #         'img_id': photo_id,
    #         'effects': effects
    #     }
    #     response = self.client.post(
    #         '/api/photos/' + str(img_id) + '/preview/', data)
    #     return self.decode_json(response)

    # def test_img_update(self):
    #     """ Test images can be updated"""
    #     response = self.upload_photo(self.client)
    #     result = self.decode_json(response)
    #     img_id = result.get('id', 0)
    #     response = self.client.put(
    #         '/api/images/' + str(img_id) + '/', {'effects': 'blur'})
    #     result = self.decode_json(response)
    #     self.assertEqual(result.get('id'), img_id)
    #     self.assertEqual(result.get('effects'), 'blur')

    # @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    # def test_upload_image_to_api_endpoint(self):
    #     """ Test a user can upload an image"""
    #     temp = tempfile.NamedTemporaryFile(suffix=".jpg").name
    #     test_image = get_temporary_image(temp)
    #     with open(test_image) as image:
    #         response = self.client.post(
    #             '/api/images/',
    #             {'image': image},
    #             format='application/json'
    #         )
    #     self.assertEqual(response.status_code, 201)

    # def test_all_images_are_retrieved(self):
    #     """Test for retrieving all the images"""
    #     response = self.client.get(reverse(image-list))
    #     self.assertEqual(response.status_code, 200)    

#     def test__downloading_image(self):
#         """ Test user can download images they have edited"""
#         response = self.upload_photo(self.client)
#         result = self.decode_json(response)
#         img_id = result.get('id', 0)
#         response = self.client.get('/download?image=' + str(img_id))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_img_deletion(self):
#         """ Test use can delete images """
#         response = self.upload_photo(self.client)
#         result = self.decode_json(response)
#         img_id = result.get('id', 0)
#         response = self.client.delete('/api/photos/' + str(img_id) + '/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


#     def test_display_of_images(self):
#         """ Test all images are displayed on get request"""
#         self.upload_photo(self.client)
#         response = self.client.get('/api/photos/')
#         result = self.decode_json(response)
#         self.assertEqual(result.get('count'), 1)

#     def test_folder_list_photos(self):
#         """Test user can view folder per folder"""
#         response = create_folder(self.client, 'test')
#         result = self.decode_json(response)
#         folder_id = result.get('id', 0)
#         self.upload_photo(self.client, folder_id)
#         response = self.client.get(
#             '/api/folders/' + str(folder_id) + '/photos/')
#         result = self.decode_json(response)
#         self.assertEqual(result.get('count'), 1)

#     def test_folder_list_untitled_photos(self):
#         """ Test that an untitled folder can contain images"""
#         self.upload_photo(self.client)
#         self.upload_photo(self.client)
#         response = self.client.get('/api/folders/0/photos/')
#         result = self.decode_json(response)
#         self.assertEqual(result.get('count'), 1)

#     def test_photo_effect_update(self):
#         """ Test user can update effects on images"""
#         response = self.upload_photo(self.client)
#         result = self.decode_json(response)
#         img_id = result.get('id', 0)
#         data = {
#             'title': 'update img effect',
#             'effects': '{"enhance":{"Brightness":"65"},"filter":{"blur":"true"},"transform":{"mirror":"true"},"effect":{"quantize":"50","gaussian_blur":"50","auto_contrast":"50","posterize":"50","unsharp_mask":"50","solarize":"50","remove_border":"50","rotate":"50"}}'
#         }
#         response = self.client.put('/api/photos/' + str(img_id) + '/', data)
#         result = self.decode_json(response)
#         self.assertEqual(result.get('title'), 'update img effect')

#     def test_photo_effect_preview(self):
#         """ Test user can preview efects to be applied on images"""
#         response = self.upload_photo(self.client)
#         result = self.photo_effect(
#             '{"transform":{"vertical_flip":"true","invert":"true","grayscale":"true","black_and_white":"true","equalize":"true"}}')
#         applied_effect = 'invert' in result.get('applied_effects', [])
#         self.assertNotEqual(result.get('image'), None)
#         self.assertTrue(applied_effect)

#     def test_text_overlay_on_images(self):
#         """ Test user can append text on images"""
#         response = self.upload_photo(self.client)
#         result = self.photo_effect(
#             '{"text_overlay":{"textValue":"love is key","fontSize":"26","x":"22","y":"24","color":"#ff3400","font_name":"dahot2.Filxgirl.ttf"}}')
#         applied_effect = 'text' in result.get('applied_effects', [])
#         self.assertTrue(applied_effect)
#         self.assertNotEqual(result.get('image'), '')
#         self.assertNotEqual(result.get('image'), None)

#     def test_photo_effect_colorize(self):
#         """ Test user can colorize images"""
#         response = self.upload_photo(self.client)
#         result = self.photo_effect(
#             '{"colorize":{"black":"#5f1212","white":"#8b572a"}}')
#         applied_effect = 'colorize' in result.get('applied_effects', [])
#         self.assertTrue(applied_effect)
#         self.assertNotEqual(result.get('image'), '')
#         self.assertNotEqual(result.get('image'), None)

#     def test_photo_effect_border(self):
#         """ Test user can apply border effect"""
#         response = self.upload_photo(self.client)
#         result = self.photo_effect(
#             '{"border":{"size":"26","border_color":"#ff3737"}}')
#         applied_effect = 'border' in result.get('applied_effects', [])
#         self.assertTrue(applied_effect)
#         self.assertNotEqual(result.get('image'), '')
#         self.assertNotEqual(result.get('image'), None)

#     def test_photo_share(self):
#         """ Test user can share photoes"""
#         response = self.upload_photo(self.client)
#         result = self.decode_json(response)
#         share_id = result.get('share_code', '')
#         response = self.client.get('/api/photos/share/?share_id=' + share_id)
#         result = self.decode_json(response)
#         self.assertEqual(result.get('share_code'), share_id)

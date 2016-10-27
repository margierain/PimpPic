import os
import json
import tempfile
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status
from django.test import override_settings
from django.core.urlresolvers import reverse
from PIL import Image
from pic.models import Photo, Folder


# Facebook graphapi test user access token
fb_token = 'EAAQp3TZCeOkkBAKpLP8KBiXgH5e70RXw4wbL16RfIYgZB2UTepIbr5lpoBDZCzaAG3hFLk4TVv4w2A4zBUqUiZBNHE2NvnkIqiICKbya0pEda2GUV1UuLNiibpyiLzQj1ajZBnAZBmO6Nelf0raiRcFKNM4xWTajhwh1MUSnoIAAZDZD'

def get_temporary_image(temp_file):
    """Generate dummy image file."""
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(temp_file, 'jpeg')
    return temp_file


def create_folder(client, name):
    """set up to create a folder"""
    data = {
        'name': name
    }
    return client.post('/api/folders/', data)


class FolderTest(APITestCase):
    """Test /api/folders/ endpoint"""


    def setUp(self):
        """Set up fb login."""
        self.user = User.objects.create(
            username='testuser', password='testpassword')
        self.uploader = User.objects.filter(id=self.user.id).first()

        data = {
            "name": "test_folder_{}".format(self.user.id),
            "creator": self.uploader
        }
        create_folder = self.client.post('/api/folders/', data)
      
    
        
    def test_get_all_images(self):
        """Test for getting all the images"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('image-list'))
        self.assertEqual(response.status_code, 200)
    

    # def test_unauthorized_access_to_folders_is_not_allowed(self):
    #     """Test that a user cannot access API without credentials."""
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Bearer facebook ' + 'auth_token')
    #     response = self.client.get(reverse('folder-list'))
    #     self.assertEqual(response.status_code, 403)
    #     detail = response.data.get('detail')
    #     self.assertIn('Invalid OAuth access token', detail)

        
    def test_folder_create(self):
        """Test user can create folders"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        self.client.force_authenticate(self.user)
        data = {
            'name': 'test_folder',
            'creator': self.uploader
        }
        response = self.client.post('/api/folders/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_all_folder(self):
        """Test all folder can be retrieved by a user """
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('folder-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)    


    # def test_unauthorized_access_to_images_is_not_allowed(self):
    #     """Test that a user cannot access API without credentials."""
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Bearer facebook ' + 'auth_token')
    #     response = self.client.get('/api/images/')
    #     self.assertEqual(response.status_code, 403)
    #     detail = response.data.get('detail')
    #     self.assertIn('Invalid OAuth access token', detail)
    
    
    def test_folder_update(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        self.client.force_authenticate(self.user)
        response = create_folder(self.client, 'test')
        folder_id = response.data.get('id', 0)
        data = {
            'name':'test edit'
        }
        response = self.client.put('/api/folders/' + str(folder_id) + '/', data)
        self.assertEqual(response.data.get('name'), 'test edit')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
   
        

    def test_folder_delete(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        self.client.force_authenticate(self.user)
        response = create_folder(self.client, 'test')
        folder_id = response.data.get('id', 0)
        response = self.client.delete('/api/folders/' + str(folder_id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    



# class ImageTest(APITestCase):
#     """Test /api/pics/ endpoint """

#     def setUp(self):
#         """Set up base user and details for test running."""
#         self.user = User.objects.create(
#             username='testuser', password='testpassword')
#         self.uploader = User.objects.filter(id=self.user.id).first()
#         temp = tempfile.NamedTemporaryFile(suffix=".jpg").name
           


#     def photo_effect(self, effects):
#         response = create_photo(self.client)
#         result = self.decode_json(response)
#         img_id = result.get('id', 0)
#         data = {
#             'img_id': photo_id,
#             'effects': effects,
#             'uploader': self.uploader
#         }
#         response = self.client.post('/api/images/' + str(img_id), data)
#         return self.decode_json(response)


#     def test_photo_create_without_folder(self):
#         # self.client.force_authenticate(self.user)
#         self.client.credentials(
#             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#         response = create_photo(self.client)
#         self.assertEqual(response.status_code, 201)
            
#     def test_img_filters_to_blur(self):
#         """ Test images can be updated"""
#         self.client.credentials(
#             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#         response = create_photo(self.client)
#         img_id = response.data.get('id', 0)
#         data = {
#             'effects':'{"filter":"blur"}'
#         }
#         response = self.client.put(
#             '/api/images/' + str(img_id) + '/', data)
#         self.assertEqual(response.data.get('id'), img_id)
#         self.assertIn(str(response.data.get('effects')), '{"filter":"blur"}')

        
#     def test_img_effect_sharpness(self):
#         """ Test images can be updated"""
#         self.client.credentials(
#             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#         response = create_photo(self.client)
#         img_id = response.data.get('id', 0)
#         data = {
            
#             'effects':'{"enhance":["Sharpness","7"]}'
#         }
#         response = self.client.put(
#             '/api/images/' + str(img_id) + '/', data)
#         self.assertEqual(response.data.get('id'), img_id)
#         self.assertIn(str(response.data.get('effects')), '{"enhance":["Sharpness","7"]}')

#     def test_img_effect_quantize(self):
#             """ Test images can be updated"""
#             self.client.credentials(
#                 HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#             response = create_photo(self.client)
#             img_id = response.data.get('id', 0)
#             data = {
                
#                 'effects':'{"effect":["quantize","5"]}'
#             }
#             response = self.client.put(
#                 '/api/images/' + str(img_id) + '/', data)
#             self.assertEqual(response.data.get('id'), img_id)
#             self.assertIn(str(response.data.get('effects')), '{"effect":["quantize","5"]}')
            
#     def test_img_effect_gaussian_blur(self):
#             """ Test images can be updated"""
#             self.client.credentials(
#                 HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#             response = create_photo(self.client)
#             img_id = response.data.get('id', 0)
#             data = {
                
#                 'effects':'{"effect":["gaussian_blur","5"]}'
#             }
#             response = self.client.put(
#                 '/api/images/' + str(img_id) + '/', data)
#             self.assertEqual(response.data.get('id'), img_id)
#             self.assertIn(str(response.data.get('effects')), '{"effect":["gaussian_blur","5"]}')

#     def test_img_posterize_effect(self):
#             """ Test images can be updated"""
#             self.client.credentials(
#                 HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#             response = create_photo(self.client)
#             img_id = response.data.get('id', 0)
#             data = {
                
#                 'effects':'{"effect":["posterize","5"]}'
#             }
#             response = self.client.put(
#                 '/api/images/' + str(img_id) + '/', data)
#             self.assertEqual(response.data.get('id'), img_id)
#             self.assertIn(str(response.data.get('effects')), '{"effect":["posterize","5"]}')

#     def test_img_rotates(self):
#             """ Test images can be updated"""
#             self.client.credentials(
#                 HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#             response = create_photo(self.client)
#             img_id = response.data.get('id', 0)
#             data = {
                
#                 'effects':'{"effect":["rotate","5"]}'
#             }
#             response = self.client.put(
#                 '/api/images/' + str(img_id) + '/', data)
#             self.assertEqual(response.data.get('id'), img_id)
#             self.assertIn(str(response.data.get('effects')), '{"effect":["rotate","5"]}') 

#     def test_img_rotates(self):
#         """ Test images can be updated"""
#         self.client.credentials(
#             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#         response = create_photo(self.client)
#         img_id = response.data.get('id', 0)
#         data = {
            
#             'effects': '{"enhance":["Contrast","7"]}'
#         }
#         response = self.client.put(
#             '/api/images/' + str(img_id) + '/', data)
#         self.assertEqual(response.data.get('id'), img_id)
#         self.assertIn(str(response.data.get('effects')), '{"enhance":["Contrast","7"]}') 

          

#     def test_img_transformation(self):
#         """ Test images can be updated"""
#         self.client.credentials(
#             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#         response = create_photo(self.client)
#         img_id = response.data.get('id', 0)
#         data = {
#              'effects': '{"transform":"black_and_white"}'
#         }
#         response = self.client.put(
#             '/api/images/' + str(img_id) + '/', data)
#         self.assertEqual(response.data.get('id'), img_id)
#         self.assertIn(str(response.data.get('effects')), '{"transform":"black_and_white"}')  
                    

#     def test_login_successful(self):
#         """Test that a GET to api/login/(?P<backend>[^/]+)/ logins user successfully"""

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
#         response = self.client.get(
#             "/login/facebook/?access_token=" + fb_token)
#         self.assertEqual(302, response.status_code)


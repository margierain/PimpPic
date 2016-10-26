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
fb_token = 'EAAQp3TZCeOkkBAG4KMAvSpChKz1vZBu9nqX1Y9O52kaIMfvEeksgZANP4oToklhr950Gryd3UURRM7QJ972y2LtGk7mVo0i6RQv8hbR1lWj0JI0QhibXfLSl5BNtP1w78ZBBUXPPTjWsXnnoyD6Dce3mVZBI1fwnyiaiHwpiZBHgZDZD'


# def create_folder(client, name):
#     """set up to create a folder"""
#     data = {
#         'name': name
#     }
#     return client.post('/api/folders/', data)

def create_photo(client, folder_id=0):
    """set up to upload image"""
    path = os.path.join(os.path.dirname(__file__), 'op3.jpeg')
    with open(path) as photo:
        data = {
            'image': photo,
            'folder_id':folder_id
        }
        return client.post('/api/images/', data)
    return None    

class FolderTest(APITestCase):
    """Test /api/folders/ endpoint"""


    def setUp(self):
        """Set up fb login."""
        self.client.credentials(
             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        self.client.get("/login/facebook/?access_token=" + fb_token)
        user = User.objects.create(
            username='testuser', password='testpassword')
        self.uploader = User.objects.filter(id=user.id).first()

        # data = {
        #     'name': 'test_folder'
        # }
        # create_folder = Folder.objects.create(name="test_folder", creator=self.uploader)
        data = {
            "name": "test_folder_{}".format(user.id),
            "creator": self.uploader
        }
        # create_folder = self.client.post('/api/folders/', data)
      
    
    # def tearDown(self):
    #     """Delete user modal after use"""
    #     del user
        
           
        
    def test_get_all_images(self):
        """Test for getting all the images"""
        self.client.credentials(
             HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        response = self.client.get('/api/images/')
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
            'name': 'test_folder_2',
            'creator': self.uploader
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
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
    #     response = create_folder(self.client, 'test')
    #     result = decode_json(response)
    #     folder_id = result.get('id', 0)
    #     response = self.client.put('/api/folders/' + str(folder_id) + '/', {'name':"test edit"})
    #     result = decode_json(response)
    #     self.assertEqual(result.get('name'), 'test edit')
   
        

    # def test_folder_delete(self):
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
    #     response = create_folder(self.client, 'test')
    #     result = decode_json(response)
    #     folder_id = result.get('id', 0)
    #     response = self.client.delete('/api/folders/' + str(folder_id) + '/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    



class ImageTest(APITestCase):
    """Test /api/pics/ endpoint """

    def setUp(self):
        """Set up base user and details for test running."""
        user = User.objects.create(
            username='testuser', password='testpassword')
        self.uploader = User.objects.filter(id=user.id).first()
        temp = tempfile.NamedTemporaryFile(suffix=".jpg").name
           


    def photo_effect(self, effects):
        response = create_photo(self.client)
        result = self.decode_json(response)
        img_id = result.get('id', 0)
        data = {
            'img_id': photo_id,
            'effects': effects,
            'uploader': self.uploader
        }
        response = self.client.post('/api/images/' + str(img_id), data)
        return self.decode_json(response)


    def test_photo_create_without_folder(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        response = create_photo(self.client)
        self.assertEqual(response.status_code, 201)
            
    def test_img_filters_to_blur(self):
        """ Test images can be updated"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        response = create_photo(self.client)
        img_id = response.data.get('id', 0)
        data = {
            'effects':'{"filter":"blur"}'
        }
        response = self.client.put(
            '/api/images/' + str(img_id) + '/', data)
        self.assertEqual(response.data.get('id'), img_id)
        self.assertIn(str(response.data.get('effects')), '{"filter":"blur"}')

        
    def test_img_effect_sharpness(self):
        """ Test images can be updated"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        response = create_photo(self.client)
        img_id = response.data.get('id', 0)
        data = {
            
            'effects':'{"enhance":["Sharpness","7"]}'
        }
        response = self.client.put(
            '/api/images/' + str(img_id) + '/', data)
        self.assertEqual(response.data.get('id'), img_id)
        self.assertIn(str(response.data.get('effects')), '{"enhance":["Sharpness","7"]}')

    def test_img_effect_quantize(self):
            """ Test images can be updated"""
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
            response = create_photo(self.client)
            img_id = response.data.get('id', 0)
            data = {
                
                'effects':'{"effect":["quantize","5"]}'
            }
            response = self.client.put(
                '/api/images/' + str(img_id) + '/', data)
            self.assertEqual(response.data.get('id'), img_id)
            self.assertIn(str(response.data.get('effects')), '{"effect":["quantize","5"]}')
            
    def test_img_effect_gaussian_blur(self):
            """ Test images can be updated"""
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
            response = create_photo(self.client)
            img_id = response.data.get('id', 0)
            data = {
                
                'effects':'{"effect":["gaussian_blur","5"]}'
            }
            response = self.client.put(
                '/api/images/' + str(img_id) + '/', data)
            self.assertEqual(response.data.get('id'), img_id)
            self.assertIn(str(response.data.get('effects')), '{"effect":["gaussian_blur","5"]}')

    def test_img_posterize_effect(self):
            """ Test images can be updated"""
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
            response = create_photo(self.client)
            img_id = response.data.get('id', 0)
            data = {
                
                'effects':'{"effect":["posterize","5"]}'
            }
            response = self.client.put(
                '/api/images/' + str(img_id) + '/', data)
            self.assertEqual(response.data.get('id'), img_id)
            self.assertIn(str(response.data.get('effects')), '{"effect":["posterize","5"]}')

    def test_img_rotates(self):
            """ Test images can be updated"""
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
            response = create_photo(self.client)
            img_id = response.data.get('id', 0)
            data = {
                
                'effects':'{"effect":["rotate","5"]}'
            }
            response = self.client.put(
                '/api/images/' + str(img_id) + '/', data)
            self.assertEqual(response.data.get('id'), img_id)
            self.assertIn(str(response.data.get('effects')), '{"effect":["rotate","5"]}') 

    def test_img_rotates(self):
        """ Test images can be updated"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        response = create_photo(self.client)
        img_id = response.data.get('id', 0)
        data = {
            
            'effects': '{"enhance":["Contrast","7"]}'
        }
        response = self.client.put(
            '/api/images/' + str(img_id) + '/', data)
        self.assertEqual(response.data.get('id'), img_id)
        self.assertIn(str(response.data.get('effects')), '{"enhance":["Contrast","7"]}') 

          

    def test_img_transformation(self):
        """ Test images can be updated"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        response = create_photo(self.client)
        img_id = response.data.get('id', 0)
        data = {
             'effects': '{"transform":"black_and_white"}'
        }
        response = self.client.put(
            '/api/images/' + str(img_id) + '/', data)
        self.assertEqual(response.data.get('id'), img_id)
        self.assertIn(str(response.data.get('effects')), '{"transform":"black_and_white"}')  
                    

    def test_login_successful(self):
        """Test that a GET to api/login/(?P<backend>[^/]+)/ logins user successfully"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer facebook ' + fb_token)
        response = self.client.get(
            "/login/facebook/?access_token=" + fb_token)
        self.assertEqual(302, response.status_code)

    # def tearDown(self):
    #     """Delete user modal after use"""
    #     del self.user
        

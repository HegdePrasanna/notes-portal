from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, Token, AccessToken
import pdb

from .models import User, Role

# Create your tests here.
class TestSetup(APITestCase):
    def setUp(self):
        user_object = User.objects.create(username='testuser001', password='testpassword', email='testmail001@mail.com', is_superuser=True)
        self.refresh = AccessToken.for_user(user_object)
        # self.api_client = APIClient()
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    

class TestRoleGetCreate(TestSetup):
    def test_create_role_without_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.post(reverse('get_create_roles'))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 400)
        self.assertEqual(res.data['data'], [])

    
    def test_create_role_with_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        data = {
            "name":"TestRole001"
        }
        res = self.client.post(reverse('get_create_roles'), data=data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 201)
    
    def test_edit_role_with_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        new_role = Role.objects.create(name='TestRole001')
        update_data = {
            "name":"TestRole001"
        }
        res = self.client.put(reverse('get_put_delete_role', kwargs={'pk': new_role.id}), data=update_data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)
    
    
    def test_edit_role_with_data_wo_superuser(self):
        new_user = User.objects.create(username='testuser004', password='testpassword', email='testmail001@mail.com')
        refresh = AccessToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
        new_role = Role.objects.create(name='TestRole001')
        update_data = {
            "name":"TestRole001"
        }
        res = self.client.put(reverse('get_put_delete_role', kwargs={'pk':new_role.id}), data=update_data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 401)
    
    def test_edit_role_with_data_wo_role(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        new_role = Role.objects.create(name='TestRole001')
        update_data = {
            "name":"TestRole001"
        }
        res = self.client.put(reverse('get_put_delete_role', kwargs={'pk':100002}), data=update_data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 404)

    def test_get_all_roles_wo_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.get(reverse('get_create_roles'))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 404)
    
    def test_get_all_roles(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        Role.objects.create(name="TestRole002")
        res = self.client.get(reverse('get_create_roles'))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)

    def test_get_single_role_w_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        role = Role.objects.create(name="TestRole002")
        res = self.client.get(reverse('get_put_delete_role', kwargs={'pk': role.id}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)
    
    def test_get_single_role_wo_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        role = Role.objects.create(name="TestRole002")
        res = self.client.get(reverse('get_put_delete_role', kwargs={'pk': 10001}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 404)
    
    def test_delete_single_role_w_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        role = Role.objects.create(name="TestRole002")
        res = self.client.delete(reverse('get_put_delete_role', kwargs={'pk': role.id}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)


class TestCreateNewUser(TestSetup):
    def test_create_new_user_wo_data(self):
        res = self.client.post(reverse('create_user'))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 400)
        self.assertEqual(res.data['data'], [])

    def test_create_new_user_w_correct_data(self):
        data = {
            "username":"testuser002",
            "email":"testuser002@example.com",
            "password":"12345"
        }
        res = self.client.post(reverse('create_user'), data=data, format='json')
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 201)
    
    def test_create_new_user_w_incorrect_data_1(self):
        data = {
            "username":"testuser002",
            "email":"testuser003@example.com",
            "password":"12345"
        }
        res = self.client.post(reverse('create_user'), data=data, format='json')
        data = {
            "username":"testuser002",
            "email":"testuser003@example.com",
            "password":"12345"
        }
        res = self.client.post(reverse('create_user'), data=data, format='json')
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 400)


class TestGetUserDetails(TestSetup):
    def test_get_all_users(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.get(reverse('get_user'))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)

    def test_get_user_by_id(self):
        new_user = User.objects.create(username='testuser003', password='testpassword', email='testmail001@mail.com')
        refresh = AccessToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
        res = self.client.get(reverse('get_put_delete_user',  kwargs={'pk': new_user.id}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)
    
    def test_get_user_by_wrong_id(self):
        # new_user = User.objects.create(username='testuser003', password='testpassword', email='testmail001@mail.com')
        # refresh = AccessToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.get(reverse('get_put_delete_user',  kwargs={'pk': 100082}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 404)
    
    def test_edit_user_by_wrongid(self):
        new_user = User.objects.create(username='testuser003', password='testpassword', email='testmail001@mail.com')
        refresh = AccessToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
        update_data = {
            "email":"testmailupdate002@mail.com"
        }
        res = self.client.put(reverse('get_put_delete_user', kwargs={'pk': 100082}), data = update_data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 404)
    
    def test_edit_user_by_id(self):
        new_user = User.objects.create(username='testuser003', password='testpassword', email='testmail001@mail.com')
        refresh = AccessToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
        update_data = {
            "email":"testmailupdate002@mail.com"
        }
        res = self.client.put(reverse('get_put_delete_user', kwargs={'pk': new_user.id}), data = update_data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)
    
    def test_edit_user_pw_by_id(self):
        new_user = User.objects.create(username='testuser003', password='testpassword', email='testmail001@mail.com')
        refresh = AccessToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
        update_data = {
            "email":"testmailupdate002@mail.com",
            "password":"123456"
        }
        res = self.client.put(reverse('get_put_delete_user', kwargs={'pk': new_user.id}), data = update_data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)

    def test_disable_user_by_wrongid(self):
        new_user = User.objects.create(username='testuser003', password='testpassword', email='testmail001@mail.com')
        refresh = AccessToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
        
        res = self.client.put(reverse('get_put_delete_user', kwargs={'pk': 100082}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 404)
    
    def test_disable_user_by_id(self):
        new_user = User.objects.create(username='testuser003', password='testpassword', email='testmail001@mail.com')
        refresh = AccessToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
        
        res = self.client.delete(reverse('get_put_delete_user', kwargs={'pk': new_user.id}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)

from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, Token, AccessToken
import pdb

from .models import Notes, User

class TestSetup(APITestCase):
    def setUp(self):
        self.user_object = User.objects.create(username='testuser001', password='testpassword', email='testmail001@mail.com', is_superuser=True)
        self.refresh = AccessToken.for_user(self.user_object)
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()


class TestCreateNotes(TestSetup):
    def test_get_all_notes_wo_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.get(reverse('get_all_notes'))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 404)
    

    def test_get_all_notes_w_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        Notes.objects.create(note_content='Test Note', created_by=self.user_object,modified_by=self.user_object)
        res = self.client.get(reverse('get_all_notes'))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)

    def test_create_new_notes_wo_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.post(reverse('create_notes'))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 400)
    
    def test_create_new_notes_w_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        data = {
            "note_content": "Test Note Create",
            "is_active": True
        }
        res = self.client.post(reverse('create_notes'), data=data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 201)


class TestNoteGetEdit(TestSetup):
    
    # random_user = User.objects.create(username='testrandomuser002', password='testpassword', email='testrandomuser002@mail.com')
    # random_refresh = AccessToken.for_user(random_user)
    
    def test_get_note_wo_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.get(reverse('get_notes', kwargs={"note_id":10002}))
        # pdb.set_trace()
        self.assertEqual(res.status_code, 404)
    
    def test_get_note_w_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')

        data = {
            "note_content": "Test Note Create",
            "is_active": True
        }
        note_create = self.client.post(reverse('create_notes'), data=data)
        note_id = note_create.data.get('data').get('id')
       
        res = self.client.get(reverse('get_notes', kwargs={"note_id":note_id}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)
    
    def test_get_note_wo_data_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.get(reverse('get_detailed_notes', kwargs={"note_id":10002}))
        # pdb.set_trace()
        self.assertEqual(res.status_code, 404)
    
    def test_get_note_w_data_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')

        data = {
            "note_content": "Test Note Create",
            "is_active": True
        }
        note_create = self.client.post(reverse('create_notes'), data=data)
        note_id = note_create.data.get('data').get('id')
       
        res = self.client.get(reverse('get_detailed_notes', kwargs={"note_id":note_id}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)

    def test_edit_note_wo_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        data = {
            "note_content": "Test Note Create",
            "is_active": True
        }
        note_create = self.client.post(reverse('create_notes'), data=data)
        note_id = note_create.data.get('data').get('id')
        edit_data = {
            "note_content":""
        }
        res = self.client.put(reverse('get_notes', kwargs={"note_id":note_id}), data=edit_data)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 400)
    
    def test_edit_note_w_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        data = {
            "note_content": "Test Note Create",
            "is_active": True
        }
        note_create = self.client.post(reverse('create_notes'), data=data)
        note_id = note_create.data.get('data').get('id')

        edit_data = {
            "note_content": "Test Note Edit"
        }
        res = self.client.put(reverse('get_notes', kwargs={"note_id":note_id}),data=edit_data)
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)
    
    def test_delete_note_wo_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        data = {
            "note_content": "Test Note Create",
            "is_active": True
        }
        note_create = self.client.post(reverse('create_notes'), data=data)
        note_id = note_create.data.get('data').get('id')
       
        res = self.client.delete(reverse('get_notes', kwargs={"note_id":1002}))
        # pdb.set_trace()
        self.assertEqual(res.status_code, 404)
    
    def test_delete_note_w_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        data = {
            "note_content": "Test Note Create",
            "is_active": True
        }
        note_create = self.client.post(reverse('create_notes'), data=data)
        note_id = note_create.data.get('data').get('id')
       
        res = self.client.delete(reverse('get_notes', kwargs={"note_id":note_id}))
        # pdb.set_trace()
        self.assertEqual(res.data['status'], 200)


class TestShareNotes(TestSetup):
    def create_notes(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')

        data = {
            "note_content": "Test Note Create for Share",
            "is_active": True
        }
        note_create = self.client.post(reverse('create_notes'), data=data, format='json')
        note_id = note_create.data.get('data').get('id')
        return note_id
    
    def create_user(self):
        another_user = User.objects.create(username='testrandomuser003', password='testpassword', email='testrandomuser003@mail.com')
        refresh_token = AccessToken.for_user(another_user)
        return another_user.id, refresh_token

    def test_share_notes(self):
        new_note = self.create_notes()
        new_user, refresh_token = self.create_user()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        # with Basic Permission
        data = [{
            "notes": new_note,
            "user": new_user
        }]
        new_note_share = self.client.post(reverse('share_notes'), data=data, format='json')
        # pdb.set_trace()
        self.assertEqual(new_note_share.status_code, 200)

        # Update the permission
        data = [{
            "notes": new_note,
            "user": new_user,
            "can_edit": True,
            "can_delete":True
        }]
        update_note = self.client.post(reverse('share_notes'), data=data, format='json')
        # pdb.set_trace()
        self.assertEqual(update_note.status_code, 200)
        
        # Improper Data
        data = [{
            "notes": new_note,
            "can_edit": True,
            "can_delete":True
        }]
        note_input_incorrect = self.client.post(reverse('share_notes'), data=data, format='json')
        error_data = note_input_incorrect.data.get('data', {}).get('validation_errors', None)
        # pdb.set_trace()
        self.assertIsNotNone(error_data)

    def test_read_edit_notes_wo_permission(self):
        new_note = self.create_notes()
        new_user, refresh_token = self.create_user()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')

        # Update the permission
        create_data = [{
            "notes": new_note,
            "user": new_user,
            "can_edit": False,
            "can_delete":False,
            "can_read":False,
        }]

        update_note = self.client.post(reverse('share_notes'), data=create_data, format='json')
        data = [{
            "notes": new_note,
            "user": new_user
        }]

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token}')
        read_notes = self.client.get(reverse('get_notes', kwargs={'note_id': new_note}))
        # pdb.set_trace()
        self.assertEqual(read_notes.status_code, 403)

        edit_note = self.client.put(reverse('get_notes', kwargs={'note_id': new_note}), data=data, format='json')
        # pdb.set_trace()
        self.assertEqual(edit_note.status_code, 403)

        edit_note = self.client.delete(reverse('get_notes', kwargs={'note_id': new_note}))
        # pdb.set_trace()
        self.assertEqual(edit_note.status_code, 403)

class TestVersionHistory(TestSetup):
    def update_note(self, note_id):
        edit_data = {
            "note_content": "Test Note Edit"
        }
        res = self.client.put(reverse('get_notes', kwargs={"note_id":note_id}), data=edit_data)
        # pdb.set_trace()
        return res

    def create_notes(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')

        data = {
            "note_content": "Test Note Create for Share",
            "is_active": True
        }
        note_create = self.client.post(reverse('create_notes'), data=data, format='json')
        note_id = note_create.data.get('data').get('id')
        return note_id
    
    def test_get_version_history_wo_note(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        res = self.client.get(reverse('get_history', kwargs={"note_id":100003}))
        # pdb.set_trace()
        self.assertEqual(res.status_code, 404)
    
    def test_get_version_history_wo_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        new_note_id = self.create_notes()
        
        # Get without history
        res = self.client.get(reverse('get_history', kwargs={"note_id": new_note_id}))
        # pdb.set_trace()
        self.assertEqual(res.status_code, 200)

    def test_get_version_history_w_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh}')
        new_note_id = self.create_notes()
        update_note = self.update_note(new_note_id)
        
        # Get without history
        res = self.client.get(reverse('get_history', kwargs={"note_id": new_note_id}))
        # pdb.set_trace()
        self.assertEqual(res.status_code, 200)

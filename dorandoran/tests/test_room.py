from django.test import TestCase, Client
from rest_framework import status
from room.models import Room
from account.models import User
from django.contrib.auth.hashers import make_password

import json


client = Client()

class RoomCreate(TestCase):

    def setUp(self):

        normal_user = { 
            "name" : "seojin",
            "email" : "seojin@gmail.com",
            "password" : make_password("0128gksqls"),
        }
        User.objects.create(**normal_user)

        teacher_user = { 
            "name" : "teacher",
            "email" : "teacher@gmail.com",
            "password" : make_password("0128gksqls"),
            "is_teacher" : True
        }
        User.objects.create(**teacher_user)

        self.base_room_form = {
            "name":"class2",
            "max_team":2,
        }

        response = client.post(
            "/auth/login", normal_user,
            content_type="application/json"
        )

        self.student_token = response.json()["token"]

        response = client.post(
            "/auth/login", teacher_user,
            content_type="application/json"
        )

        self.teacher_token = response.json()["token"]

    def tearDown(self):
        Room.objects.all().delete()
        User.objects.all().delete()

    def test_create_room_success(self):
        room = self.base_room_form

        response = client.post(
            '/room', room, content_type='application/json',
            headers={'Authorization': 'jwt {}'.format(self.teacher_token)}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_room_failed_with_incorrect_form(self):
        room = self.base_room_form
        del room['name']

        response = client.post('/room',room,content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_room_failed_with_incorrect_owner(self):
        room = self.base_room_form

        room['owner'] = 0

        response = client.post('/room',room,content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


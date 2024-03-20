from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from .models import *
from .views import *


class TestCreateUser(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('api/create_user')
        self.view = create_user

    @patch('User.objects')
    @patch('UserSerializer')
    @patch('DaterSerializer')
    @patch('CupidSerializer')
    def test_create_user_good(self, mock_user_objects, mock_user_serializer,
                              mock_dater_serializer, mock_cupid_serializer):
        # Test 1: create dater
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = True
        mock_user_serializer.save.return_value = None
        mock_dater_serializer.is_valid.return_value = True
        mock_dater_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Dater',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert mock_user_serializer.called
        assert mock_dater_serializer.called
        assert not mock_cupid_serializer.called
        assert mock_user_serializer.save.called
        assert mock_dater_serializer.save.called

        # Test 2: create cupid
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = True
        mock_user_serializer.save.return_value = None
        mock_cupid_serializer.is_valid.return_value = True
        mock_cupid_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Cupid',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert mock_user_serializer.called
        assert mock_cupid_serializer.called
        assert not mock_dater_serializer.called
        assert mock_user_serializer.save.called
        assert mock_cupid_serializer.save.called

    @patch('User.objects')
    @patch('UserSerializer')
    @patch('DaterSerializer')
    @patch('CupidSerializer')
    def test_create_user_bad(self, mock_user_objects, mock_user_serializer,
                             mock_dater_serializer, mock_cupid_serializer):
        # Test 1: create dater with missing password
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_dater_serializer.is_valid.return_value = False
        mock_dater_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Dater',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_dater_serializer.called
        assert not mock_cupid_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_dater_serializer.save.called

        # Test 2: create dater with missing role
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_dater_serializer.is_valid.return_value = False
        mock_dater_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_dater_serializer.called
        assert not mock_cupid_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_dater_serializer.save.called

        # Test 3: create dater with invalid role
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_dater_serializer.is_valid.return_value = False
        mock_dater_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'test',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_dater_serializer.called
        assert not mock_cupid_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_dater_serializer.save.called

        # Test 4: create dater with invalid email
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_dater_serializer.is_valid.return_value = False
        mock_dater_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Dater',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_dater_serializer.called
        assert not mock_cupid_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_dater_serializer.save.called

        # Test 5: create dater with invalid username
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_dater_serializer.is_valid.return_value = False
        mock_dater_serializer.save.return_value = None
        # set up request
        data = {
            'username': '',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Dater',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_dater_serializer.called
        assert not mock_cupid_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_dater_serializer.save.called

        # Test 6: create cupid with missing password
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_cupid_serializer.is_valid.return_value = False
        mock_cupid_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Cupid',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_cupid_serializer.called
        assert not mock_dater_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_cupid_serializer.save.called

        # Test 7: create cupid with missing role
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_cupid_serializer.is_valid.return_value = False
        mock_cupid_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_cupid_serializer.called
        assert not mock_dater_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_cupid_serializer.save.called

        # Test 8: create cupid with invalid role
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_cupid_serializer.is_valid.return_value = False
        mock_cupid_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'test',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_cupid_serializer.called
        assert not mock_dater_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_cupid_serializer.save.called

        # Test 9: create cupid with invalid email
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_cupid_serializer.is_valid.return_value = False
        mock_cupid_serializer.save.return_value = None
        # set up request
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Cupid',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_cupid_serializer.called
        assert not mock_dater_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_cupid_serializer.save.called

        # Test 10: create cupid with invalid username
        # set up mocks
        mock_user_objects.get.return_value = MagicMock()
        mock_user_objects.delete.return_value = None
        mock_user_serializer.is_valid.return_value = False
        mock_user_serializer.save.return_value = None
        mock_cupid_serializer.is_valid.return_value = False
        mock_cupid_serializer.save.return_value = None
        # set up request
        data = {
            'username': '',
            'password': 'test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Cupid',
        }
        request = self.factory.post(self.url, data)
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        # make request
        response = self.view(request)
        # test response and mocks
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert mock_user_serializer.called
        assert mock_cupid_serializer.called
        assert not mock_dater_serializer.called
        assert not mock_user_serializer.save.called
        assert not mock_cupid_serializer.save.called


class TestSignIn(APITestCase):
    pass


class TestGetUser(APITestCase):
    pass


class TestUserExpand(APITestCase):
    pass


class TestDeleteUser(APITestCase):
    pass


class TestSendChatMessage(APITestCase):
    pass


class TestGetAIResponse(APITestCase):
    pass


class TestGetFiveMessages(APITestCase):
    pass


class TestCalendar(APITestCase):
    pass


class TestRateDater(APITestCase):
    pass


class TestGetDaterRating(APITestCase):
    pass


class TestGetDaterAverageRating(APITestCase):
    pass


class TestDaterTransfer(APITestCase):
    pass


class TestGetDaterBalance(APITestCase):
    pass


class TestGetDaterProfile(APITestCase):
    pass


class TestSetDaterProfile(APITestCase):
    pass


class TestRateCupid(APITestCase):
    pass


class TestGetCupidRating(APITestCase):
    pass


class TestGetCupidAverageRating(APITestCase):
    pass


class TestCupidTransfer(APITestCase):
    pass


class TestGetCupidBalance(APITestCase):
    pass


class TestGetCupidProfile(APITestCase):
    pass


class TestSetCupidProfile(APITestCase):
    pass


class TestCreateGig(APITestCase):
    pass


class TestAcceptGig(APITestCase):
    pass


class TestCompleteGig(APITestCase):
    pass


class TestDropGig(APITestCase):
    pass


class TestGetGig(APITestCase):
    pass


class TestGetLocationFromAddress(APITestCase):
    pass


class TestGetLocationFromIP(APITestCase):
    pass


class TestLocationsAreNear(APITestCase):
    pass


class TestHaversineDistance(APITestCase):
    pass


class TestWithinDistance(APITestCase):
    pass


class TestGetStores(APITestCase):
    pass


class TestGetActivities(APITestCase):
    pass


class TestGetEvents(APITestCase):
    pass


class TestGetAttractions(APITestCase):
    pass


class TestGetRestaurants(APITestCase):
    pass


class TestCallYelpAPI(APITestCase):
    pass


class TestGetUserLocation(APITestCase):
    pass


class TestGetCupids(APITestCase):
    pass


class TestGetDaters(APITestCase):
    pass


class TestGetDaterCount(APITestCase):
    pass


class TestGetCupidCount(APITestCase):
    pass


class TestGetActiveCupids(APITestCase):
    pass


class TestGetActiveDaters(APITestCase):
    pass


class TestGetGigRates(APITestCase):
    pass


class TestGetGigCount(APITestCase):
    pass


class TestGetGigDropRate(APITestCase):
    pass


class TestGetGigCompleteRate(APITestCase):
    pass


class TestSuspend(APITestCase):
    pass


class TestUnsuspend(APITestCase):
    pass


class TestSpeechToText(APITestCase):
    pass


class TestNotify(APITestCase):
    pass


class TestUpdateUserLocation(APITestCase):
    pass


class TestUserSerializer(TestCase):
    pass


class TestDaterSerializer(TestCase):
    pass


class TestCupidSerializer(TestCase):
    pass


class TestManagerSerializer(TestCase):
    pass


class TestMessageSerializer(TestCase):
    pass


class TestGigSerializer(TestCase):
    pass


class TestQueueSerializer(TestCase):
    pass


class TestDateSerializer(TestCase):
    pass


class TestFeedbackSerializer(TestCase):
    pass


class TestPaymentSerializer(TestCase):
    pass


class TestBankAccountSerializer(TestCase):
    pass


class TestUser(TestCase):
    pass


class TestDater(TestCase):
    pass


class TestCupid(TestCase):
    pass


class TestMessage(TestCase):
    pass


class TestQuest(TestCase):
    pass


class TestGig(TestCase):
    pass


class TestDate(TestCase):
    pass


class TestFeedback(TestCase):
    pass


class TestPaymentCard(TestCase):
    pass


class TestBankAccount(TestCase):
    pass

import os

from django.test import TestCase
from attacksapp.models import Attack, STATUS_CHOICES


class AttackTestCase(TestCase):
    def setUp(self):
        self.test_object = Attack.objects.create(name='test', command='test')
        self.stopped_attack = Attack.objects.create(name='stopped test', command='test',status=STATUS_CHOICES.STOPPED)

    def test_attacks_api(self):
        """
        Test attack list from api
        """
        response = self.client.get('/attacks/api')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.test_object.id)

    def test_attacks_api_post(self):
        """
        Test that a valid attack update returns a 204
        """
        response = self.client.post('/attacks/api', data={'attack_id': self.test_object.id, 'status': 'stopped'})
        self.assertEqual(response.status_code, 204)

        attack = Attack.objects.get(pk=self.test_object.id)
        self.assertEqual(attack.status, 'stopped')
        self.assertIsNone(attack.started_at)

        response = self.client.post('/attacks/api', data={'attack_id': self.test_object.id, 'status': 'running'})
        self.assertEqual(response.status_code, 204)

        attack.refresh_from_db()
        self.assertEqual(attack.status, 'running')
        self.assertIsNotNone(attack.started_at)

    def test_invalid_attack_api_id(self):
        """
        Test that an invalid attack id returns a 404
        """

        invalid_id = self.test_object.id + 1

        # test update
        response = self.client.post('/attacks/api', data={'attack_id': invalid_id, 'status': 'stopped'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Attack does not exist')

        # test get
        response = self.client.get('/attacks/api', data={'attack_id': invalid_id})
        self.assertEqual(response.status_code, 404)

    def test_get_attack_by_id(self):
        response = self.client.get('/attacks/api', data={'attack_id': self.stopped_attack.id})
        self.assertEqual(response.status_code, 200)



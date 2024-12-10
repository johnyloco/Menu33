from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from menu33.restaurants.models import Restaurant, Location

User = get_user_model()


class RestaurantEditViewTest(TestCase):
    def setUp(self):
        # Create test users
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='password123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='password123'
        )

        # Create a location and restaurant for the owner
        self.location = Location.objects.create(
            address='123 Owner Street',
            city='Owner City'
        )
        self.restaurant = Restaurant.objects.create(
            name='Owner Restaurant',
            description='Owned by the test owner.',
            location=self.location,
            user=self.owner
        )


    def test_edit_restaurant_not_owner(self):
        # Log in as another user
        self.client.login(email='other@example.com', password='password123')

        # Prepare updated data
        updated_data = {
            'name': 'Unauthorized Edit',
            'description': 'This should not be saved.',
        }

        # Send POST request
        response = self.client.post(
            reverse('restaurant-edit', args=[self.restaurant.id]),
            updated_data
        )

        # Check response
        self.assertEqual(response.status_code, 404)  # Should return 404 for unauthorized access

        # Verify that the restaurant details remain unchanged
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, 'Owner Restaurant')
        self.assertEqual(self.restaurant.description, 'Owned by the test owner.')

    def test_edit_restaurant_invalid_data(self):
        # Log in as the owner
        self.client.login(email='owner@example.com', password='password123')

        # Prepare invalid data (e.g., empty name)
        invalid_data = {
            'name': '',
            'description': 'This should fail.',
        }

        # Send POST request
        response = self.client.post(
            reverse('restaurant-edit', args=[self.restaurant.id]),
            invalid_data
        )

        # Check response
        self.assertEqual(response.status_code, 200)  # Form re-rendered on failure
        self.assertContains(response, 'This field is required.')

        # Verify that the restaurant details remain unchanged
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, 'Owner Restaurant')
        self.assertEqual(self.restaurant.description, 'Owned by the test owner.')

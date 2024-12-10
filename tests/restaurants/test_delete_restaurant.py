from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from menu33.restaurants.models import Restaurant, Location

User = get_user_model()


class RestaurantDeleteViewTest(TestCase):
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

    def test_delete_restaurant_successful(self):
        # Log in as the owner
        self.client.login(email='owner@example.com', password='password123')

        # Send POST request to delete the restaurant
        response = self.client.post(reverse('restaurant-delete', args=[self.restaurant.id]))

        # Check the response
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertRedirects(response, reverse('restaurant-list'))

        # Verify the restaurant has been deleted
        self.assertEqual(Restaurant.objects.count(), 0)

    def test_delete_restaurant_not_owner(self):
        # Log in as another user
        self.client.login(email='other@example.com', password='password123')

        # Send POST request to delete the restaurant
        response = self.client.post(reverse('restaurant-delete', args=[self.restaurant.id]))

        # Check the response
        self.assertEqual(response.status_code, 404)  # Should return 404 for unauthorized access

        # Verify the restaurant has not been deleted
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_delete_restaurant_not_logged_in(self):
        # Send POST request to delete the restaurant without logging in
        response = self.client.post(reverse('restaurant-delete', args=[self.restaurant.id]))

        # Check the response
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, f"{reverse('login-page')}?next={reverse('restaurant-delete', args=[self.restaurant.id])}")

        # Verify the restaurant has not been deleted
        self.assertEqual(Restaurant.objects.count(), 1)

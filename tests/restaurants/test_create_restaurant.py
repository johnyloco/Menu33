from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from menu33.restaurants.models import Restaurant, Location

User = get_user_model()


class RestaurantCreateViewTest(TestCase):
    def setUp(self):
        # Ensure no duplicate emails
        User.objects.filter(email='testuser@example.com').delete()

        # Create a unique test user and log in
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.client.login(email='testuser@example.com', password='password123')

    def test_create_restaurant_with_valid_data(self):
        # Prepare form data
        location_data = {
            'address': '123 Test Street',
            'city': 'Testville',
        }
        restaurant_data = {
            'name': 'Test Restaurant',
            'description': 'A place for testing.',
        }
        data = {**restaurant_data, **location_data}

        # Send POST request
        response = self.client.post(reverse('restaurant-create'), data)

        # Debugging: Print form errors if validation fails
        if response.status_code == 200:
            print(response.context['form'].errors)
            print(response.context['location_form'].errors)

        # Check the response
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertRedirects(response, reverse('restaurant-list'))

        # Check if the restaurant was created
        self.assertEqual(Restaurant.objects.count(), 1)
        restaurant = Restaurant.objects.first()
        self.assertEqual(restaurant.name, 'Test Restaurant')
        self.assertEqual(restaurant.description, 'A place for testing.')
        self.assertEqual(restaurant.user, self.user)

        # Check if the location was created
        self.assertIsNotNone(restaurant.location)
        self.assertEqual(restaurant.location.address, '123 Test Street')
        self.assertEqual(restaurant.location.city, 'Testville')

    def test_create_restaurant_with_invalid_data(self):
        # Prepare incomplete form data (missing location)
        restaurant_data = {
            'name': 'Invalid Restaurant',
            'description': 'This should not be saved.',
        }

        # Send POST request
        response = self.client.post(reverse('restaurant-create'), restaurant_data)

        # Check the response
        self.assertEqual(response.status_code, 200)  # Form is re-rendered on failure
        self.assertContains(response, 'This field is required.')

        # Ensure no restaurant or location is created
        self.assertEqual(Restaurant.objects.count(), 0)
        self.assertEqual(Location.objects.count(), 0)

    def test_delete_restaurant_not_logged_in(self):
        # Create a location and restaurant for testing
        location = Location.objects.create(
            address='123 Test Street',
            city='Testville'
        )
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            description='A place for testing.',
            location=location,
            user=self.user
        )

        # Log out and send POST request to delete the restaurant
        self.client.logout()
        response = self.client.post(reverse('restaurant-delete', args=[restaurant.id]))

        # Check the response
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('restaurant-delete', args=[restaurant.id])}")

        # Verify the restaurant has not been deleted
        self.assertEqual(Restaurant.objects.count(), 1)
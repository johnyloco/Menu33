from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from menu33.menus.models import FoodItem
from menu33.restaurants.models import Restaurant, Location

User = get_user_model()


class EditFoodItemViewTest(TestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='password123'
        )

        # Create a location and a restaurant
        self.location = Location.objects.create(
            address='123 Test Street',
            city='Test City'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            description='A place for testing.',
            location=self.location,
            user=self.user
        )

        # Create a food item for the user
        self.food_item = FoodItem.objects.create(
            name='Test Food Item',
            description='A delicious test item.',
            price=10.99,
            gluten_free=True,
            dairy_free=False,
            vegan=True,
            restaurant=self.restaurant,
            user=self.user
        )

    def test_edit_food_item_successful(self):
        # Log in as the user who created the food item
        self.client.login(email='user@example.com', password='password123')

        # Prepare updated data
        updated_data = {
            'name': 'Updated Food Item',
            'description': 'Updated description.',
            'price': 15.99,
            'gluten_free': False,
            'dairy_free': True,
            'vegan': False,
        }

        # Send POST request to edit the food item
        response = self.client.post(
            reverse('food-edit', args=[self.food_item.id]),
            data=updated_data
        )

        # Check response and redirection
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertRedirects(response, reverse('food-menu', kwargs={'restaurant_id': self.restaurant.id}))

        # Verify that the food item was updated
        self.food_item.refresh_from_db()
        self.assertEqual(self.food_item.name, 'Updated Food Item')
        self.assertEqual(self.food_item.description, 'Updated description.')
        self.assertEqual(self.food_item.price, 15.99)
        self.assertFalse(self.food_item.gluten_free)
        self.assertTrue(self.food_item.dairy_free)
        self.assertFalse(self.food_item.vegan)

    def test_edit_food_item_not_owner(self):
        # Log in as another user
        self.client.login(email='other@example.com', password='password123')

        # Prepare updated data
        updated_data = {
            'name': 'Unauthorized Edit',
            'description': 'This should not be saved.',
            'price': 20.99,
        }

        # Send POST request to edit the food item
        response = self.client.post(
            reverse('food-item-edit', args=[self.food_item.id]),
            data=updated_data
        )

        # Check response
        self.assertEqual(response.status_code, 404)  # Should return 404 for unauthorized access

        # Verify that the food item was not updated
        self.food_item.refresh_from_db()
        self.assertEqual(self.food_item.name, 'Test Food Item')
        self.assertEqual(self.food_item.description, 'A delicious test item.')
        self.assertEqual(self.food_item.price, 10.99)

    def test_edit_food_item_invalid_data(self):
        # Log in as the user who created the food item
        self.client.login(email='user@example.com', password='password123')

        # Prepare invalid data (e.g., empty name)
        invalid_data = {
            'name': '',
            'description': 'This should fail.',
            'price': -5.99,  # Invalid price
        }

        # Send POST request with invalid data
        response = self.client.post(
            reverse('food-item-edit', args=[self.food_item.id]),
            data=invalid_data
        )

        # Check response
        self.assertEqual(response.status_code, 200)  # Form should re-render on failure
        self.assertContains(response, 'This field is required.')  # Error for missing name
        self.assertContains(response, 'Ensure this value is greater than or equal to 0.')  # Error for invalid price

        # Verify that the food item was not updated
        self.food_item.refresh_from_db()
        self.assertEqual(self.food_item.name, 'Test Food Item')
        self.assertEqual(self.food_item.description, 'A delicious test item.')
        self.assertEqual(self.food_item.price, 10.99)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from menus.models import FoodItem
from restaurants.models import Restaurant, Location

User = get_user_model()


class AddFoodItemViewTest(TestCase):
    def setUp(self):
        # Create a test user and another user
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
            user=self.user  # Restaurant owned by self.user
        )

    def test_add_food_item_successful(self):
        # Log in the user
        self.client.login(email='user@example.com', password='password123')

        # Prepare valid food item data
        food_item_data = {
            'name': 'Test Food Item',
            'description': 'A delicious test item.',
            'price': 12.99,
            'gluten_free': True,
            'dairy_free': False,
            'vegan': True,
        }

        # Send POST request to add food item
        response = self.client.post(
            reverse('add-food-item', args=[self.restaurant.id]),
            data=food_item_data
        )

        # Check the response
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertRedirects(response, reverse('food-menu', kwargs={'restaurant_id': self.restaurant.id}))

        # Check that the food item was created
        self.assertEqual(FoodItem.objects.count(), 1)
        food_item = FoodItem.objects.first()
        self.assertEqual(food_item.name, 'Test Food Item')
        self.assertEqual(food_item.description, 'A delicious test item.')
        self.assertEqual(food_item.price, 12.99)
        self.assertTrue(food_item.gluten_free)
        self.assertFalse(food_item.dairy_free)
        self.assertTrue(food_item.vegan)
        self.assertEqual(food_item.restaurant, self.restaurant)
        self.assertEqual(food_item.user, self.user)

    def test_add_food_item_not_authenticated(self):
        # Prepare valid food item data
        food_item_data = {
            'name': 'Test Food Item',
            'description': 'A delicious test item.',
            'price': 12.99,
            'gluten_free': True,
            'dairy_free': False,
            'vegan': True,
        }

        # Attempt to add food item without logging in
        response = self.client.post(
            reverse('add-food-item', args=[self.restaurant.id]),
            data=food_item_data
        )

        # Check the response
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        login_url = f"{reverse('login')}?next={reverse('add-food-item', args=[self.restaurant.id])}"
        self.assertRedirects(response, login_url)

        # Verify that no food item was created
        self.assertEqual(FoodItem.objects.count(), 0)

    def test_add_food_item_invalid_data(self):
        # Log in the user
        self.client.login(email='user@example.com', password='password123')

        # Prepare invalid food item data (e.g., missing name and price)
        invalid_food_item_data = {
            'description': 'A delicious test item.',
            'gluten_free': True,
            'dairy_free': False,
            'vegan': True,
        }

        # Send POST request with invalid data
        response = self.client.post(
            reverse('add-food-item', args=[self.restaurant.id]),
            data=invalid_food_item_data
        )

        # Check response
        self.assertEqual(response.status_code, 200)  # Form should re-render on failure
        self.assertContains(response, 'This field is required.')  # Check for error message

        # Verify that no food item was created
        self.assertEqual(FoodItem.objects.count(), 0)

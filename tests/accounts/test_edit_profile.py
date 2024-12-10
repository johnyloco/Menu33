from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from menu33.accounts.models import Profile

User = get_user_model()


class ProfileEditViewTest(TestCase):
    def setUp(self):
        # Ensure no duplicate profiles
        Profile.objects.filter(user__email='owner@example.com').delete()
        Profile.objects.filter(user__email='other@example.com').delete()

        # Create test users
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='password123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='password123'
        )

        # Profile will be automatically created by a signal, or we can create it manually:
        self.profile = Profile.objects.get(user=self.owner)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.date_of_birth = '2000-01-01'
        self.profile.profile_picture = 'http://example.com/picture.jpg'
        self.profile.save()

    def test_edit_profile_successful(self):
        # Log in as the profile owner
        self.client.login(email='owner@example.com', password='password123')

        # Prepare updated profile data
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'date_of_birth': '1999-12-31',
            'profile_picture': 'http://example.com/updated_picture.jpg'
        }

        # Send POST request to update the profile
        response = self.client.post(
            reverse('profile-edit', kwargs={'pk': self.profile.pk}),
            updated_data
        )

        # Check response and redirection
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertRedirects(response, reverse('profile-details', kwargs={'pk': self.profile.pk}))

        # Verify the profile was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Updated')
        self.assertEqual(self.profile.last_name, 'Name')
        self.assertEqual(self.profile.date_of_birth.strftime('%Y-%m-%d'), '1999-12-31')
        self.assertEqual(self.profile.profile_picture, 'http://example.com/updated_picture.jpg')

    def test_edit_profile_not_owner(self):
        # Log in as another user who does not own the profile
        self.client.login(email='other@example.com', password='password123')

        # Prepare updated profile data
        updated_data = {
            'first_name': 'Unauthorized',
            'last_name': 'Access',
            'date_of_birth': '1999-12-31',
            'profile_picture': 'http://example.com/unauthorized_picture.jpg'
        }

        # Send POST request to update the profile
        response = self.client.post(
            reverse('profile-edit', kwargs={'pk': self.profile.pk}),
            updated_data
        )

        # Check response
        self.assertEqual(response.status_code, 403)  # Should return 403 Forbidden

        # Verify the profile was not updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Test')
        self.assertEqual(self.profile.last_name, 'User')
        self.assertEqual(self.profile.date_of_birth.strftime('%Y-%m-%d'), '2000-01-01')
        self.assertEqual(self.profile.profile_picture, 'http://example.com/picture.jpg')

    def test_edit_profile_invalid_data(self):
        # Log in as the profile owner
        self.client.login(email='owner@example.com', password='password123')

        # Prepare invalid profile data (e.g., missing first name)
        invalid_data = {
            'first_name': '',
            'last_name': 'Name',
            'date_of_birth': 'invalid-date',  # Invalid date format
            'profile_picture': 'http://example.com/updated_picture.jpg'
        }

        # Send POST request to update the profile
        response = self.client.post(
            reverse('profile-edit', kwargs={'pk': self.profile.pk}),
            invalid_data
        )

        # Check response
        self.assertEqual(response.status_code, 200)  # Form is re-rendered on failure
        self.assertContains(response, 'This field is required.')  # Error for first name
        self.assertContains(response, 'Enter a valid date.')  # Error for invalid date

        # Verify the profile was not updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Test')
        self.assertEqual(self.profile.last_name, 'User')
        self.assertEqual(self.profile.date_of_birth.strftime('%Y-%m-%d'), '2000-01-01')
        self.assertEqual(self.profile.profile_picture, 'http://example.com/picture.jpg')

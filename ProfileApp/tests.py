from django.test import TestCase
from django.urls import reverse  # Import reverse function
from django.contrib.auth.models import User
from ProfileApp.models import Profile, ProfileComment
import ProfileApp.urls

class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

    def test_profile_comment_creation(self):
        profile = Profile.objects.get(user=self.user)
        comment = ProfileComment.objects.create(profile=profile, user=self.user, content='Test comment')
        self.assertIsNotNone(comment)

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_search_profiles_view(self):
        response = self.client.get(reverse('ProfileApp:search_profiles'))  # Make sure 'search_profiles' is a valid URL pattern
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('ProfileApp:edit_profile'))  # Make sure 'edit_profile' is a valid URL pattern
        self.assertEqual(response.status_code, 200)  # Assuming the edit_profile view returns a 200 response for authenticated users

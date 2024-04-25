from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import IdeaBoard, IdeaBoardItem

class IdeaBoardModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.board = IdeaBoard.objects.create(title='Test Board', description='Test Description', user=self.user)
        self.item = IdeaBoardItem.objects.create(title='Test Item', description='Test Description', owner=self.user, ideaboard=self.board)

    def test_idea_board_creation(self):
        self.assertEqual(IdeaBoard.objects.count(), 1)
        self.assertEqual(self.board.title, 'Test Board')
        self.assertEqual(self.board.description, 'Test Description')
        self.assertEqual(self.board.user, self.user)

    def test_idea_board_item_creation(self):
        self.assertEqual(IdeaBoardItem.objects.count(), 1)
        self.assertEqual(self.item.title, 'Test Item')
        self.assertEqual(self.item.description, 'Test Description')
        self.assertEqual(self.item.owner, self.user)
        self.assertEqual(self.item.ideaboard, self.board)

class IdeaBoardViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.board = IdeaBoard.objects.create(title='Test Board', description='Test Description', user=self.user)
        self.item = IdeaBoardItem.objects.create(title='Test Item', description='Test Description', owner=self.user, ideaboard=self.board)

    def test_idea_boards_home_authenticated(self):
        response = self.client.get(reverse('IdeaBoards_Home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideaboard.html')
        self.assertTrue('boards' in response.context)
        self.assertTrue('form' in response.context)

    def test_idea_boards_home_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('IdeaBoards_Home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_idea_board_detail_owner(self):
        response = self.client.get(reverse('IdeaBoard_Detail', args=[self.board.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'boarddetail.html')
        self.assertTrue('board' in response.context)
        self.assertTrue('items' in response.context)

    def test_idea_board_detail_non_owner(self):
        # Create a new user who is not the owner of the board
        other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.force_login(other_user)
        response = self.client.get(reverse('IdeaBoard_Detail', args=[self.board.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('IdeaBoards_Home'))  # Non-owner is redirected to their own boards



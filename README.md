# Software-Engineering-3<br>
Introduction to the app: MediaBook is a platform to organize ideas for multimedia projects and connect with other creators. MediaBook has IdeaBoards where the user can create a board based on whatever project idea or topic they have. The user can then add and manage notes on the board to keep track of ideas for the project.  Notes can also have attached images and audio to allow users to keep track of sources of inspiration for their project. MediaBook also allows users to connect with other content creators and share ideas, tips, and give each other support through a user forum.<br>

Feature video: [![Feature video](https://img.youtube.com/vi/n8fPP22MbXU/0.jpg)](https://www.youtube.com/watch?v=n8fPP22MbXU)

IdeaBoards App: -Bilge -Nate<br>
	The IdeaBoards app exists to allow users to create idea or project boards to organize notes and ideas. Users can create boards for a desired topic and store notes on the boards.
The notes can contain image and sound files, text, and be labeled for sorting purposes. Users are also able to edit and delete items allowing for full user control on the content of a board.  Users can set a privacy setting for the board allowing others to see their project board.<br>

Views:<br>
IdeaBoard_Home: Requires use to be logged in else the user will be sent to the landing<br>
page.  Shows the logged in user all the boards they own and allows the creation <br>
of new boards.<br>
IdeaBoard_Details: Shows the user a board based on id.<br>
	If the user is ower of the board the user can add, edit, delete items on the board.  	The user can also edit the board’s name, description, and privacy settings.<br>
	The user can click on items on the board to see all the attached content
	If the user is not the owner but the board is public the user can look at all of the
	items on the board and sort items by label.
	
	The view also handled all add, edit, delete requests that effect the database.<br>
<br>
Helper functions in the ideaboard views<br>
handle_database_changes: Redirects all changes for the board to the proper functions<br>
Handle_delete_request: Handles a board delete request from the ower of a board<br>
add_item_to_board: Adds a new board item to the board with the content the user wants<br>
	to add to the item<br>
edit_item_on_board: Edits a given existing item in the database with new details using a<br>
	given item id
delete_item_on_board: deletes an item from the database based on the item id given<br>
edit_board_details: changes the title, description, and privacy settings of a given board<br>
	based on id<br>
add_label_to_database: adds a new label on a given board to the database based on<br>
	the details given by the user<br>

Models<br>
IdeaBoard -Bilge -Nate<br>
Title: title of the board (max 64 char)<br>
description: description text for the board (max 128 characters)<br>
is_public: privacy setting of the board (True = public, False = private)<br>
created_at: time board was created<br>
updated_at: time board was last edited<br>
user: points to the user who owns the board<br>
ItemLabel -Bilge<br>
label_name: name of a label (max 15 characters)<br>
label_board: board the label is on<br>
IdeaBoardItem<br>
title: title of the item (max 64 characters) <br>
description: description of the item (optional)<br>
item_image: attached image file of the item (optional) <br>
image_sound: attached sound file of the item (optional)<br>
note_label: attached label of the item (optional)<br>
created_at: time item was created<br>
updated_at: time item was last edited<br>
owner: user who owns the item/board item is on<br>
ideaboard: the board the item is on<br>
Forms<br>
NewIdeaBoardForm: Create new idea boards<br>
NewIdeaBoardItemForm: Create new items for the board<br>
NewItemLabelForm: Create new labels<br>
<br>
API/Spotify -Bilge<br>
Gets song recommendations<br>

<br>
Forum app: -Wes<br>
<br>
	The forum app exists in order to allow users of our program to interact with one another in a forum like environment. In it, users are able to create threads, post comments, subscribe to threads, receive notifications, and more. <br>
<br>
	Note, The forum app relies on the profile app, and will require modification to be usable on its own. <br>
<br>
Important views:<br>
Forum_home: The home page of the forum, This will display the top 5 most recent threads, the top 5 most commented threads, and the top 10 most recent commenters<br>
Thread_List: This view represents a list of threads that belong to a page. It will display the threads in a simple list. <br>
create_thread : View to allow a user to create a new thread, it will take in a page_id, and will create a new thread on that page<br>
Thread_detail: This view is a detailed view of a specific view, It can take in a thread_id, and a comment_id, and will display the thread, and the comments on that thread<br>
Create_comment: This view will allow the user to create a new comment on the forum. <br>
Edit_comment: This view will allow the user, or a superuser, to edit their comment. <br>
Delete_comment: This view will allow the user, or a super user to delete their comment. <br>
Like_comment: This view allows the user to like or unlike a comment not belonging to themselves. <br>
Reply_to_comment: This view allows the user to reply to an existing comment. <br>
Mark_notification_as_read: Utility view to mark a specific notification as read<br>
Notifications_page: This view will display all of the notifications the logged in user has in a paginated list. <br>
Subscribe_to_thread: This view allows a user to subscribe to a thread, so that they may receive notifications on it. <br>
Unsubscribe_from_thread: This view allows the user to unsubscribe from the thread, and they will no longer receive notifications.<br>
<br>

Utilities:<br>
Convert_media_links_to_embed: Function to convert links in text to HTML IFRAME embeds for media, Currently works for youtube and spotify links<br>
Clean_html: This function exists to attempt to remove unwanted html from the comment text. <br>

<br>

Models:<br>
<br>
Page: This model will represent a single page on the thread<br>
title: the title of the page<br>
get_latest_comment: a method that returns the latest comment in the page<br>
<br>
Thread:   The model that will represent a thread in the forum<br>
page: the page the thread is on<br>
title: the title of the thread<br>
original_poster: the user who created the thread<br>
subscribers: a list of users who have "subscribed" to the thread<br>
created_at: the time the thread was created<br>
latest_comment_time: the time of the latest comment in the thread<br>
latest_comment_username: the username of the user who made the latest comment<br>
comment_count: a property that returns the number of comments in the thread<br>
Comment: The model that will represent a comment in the forum<br>
thread: the thread the comment is on<br>
user: the user who created the comment<br>
content: the content of the comment<br>
created_at: the time the comment was created<br>
last_edited: the time the comment was last edited<br>
likes: a list of users who have liked the comment<br>
parent: the parent comment, if there is one, This is for the reply system<br>
like_count: a property that returns the number of likes the comment has<br>
Like:    The model that will represent a like on a comment<br>
comment: the comment that was liked<br>
user: the user who liked the comment<br>
created_at: the time the like was created<br>
Notification: This model will represent a notification sent to a user<br>
notification_type: the type of notification. Can be LIKE, COMMENT, or REPLY<br>
to_user: the user the notification is for<br>
from_user: the user who caused the notification<br>
thread: the thread the notification is about<br>
comment: the comment the notification is about<br>
date: the time the notification was created<br>
is_read: a boolean that represents if the notification has been read<br>



Signals<br>
Create_comment_notification: This signal will create a notification for when a user replies to a comment<br>



Context Processors:<br>
Notifications: This context processor will add the global notifications to the context of every request<br><br>




<br>


Profile App: -Wes, -Nate<br>

	This app provides a user functionality for the web app. It is tightly integrated with the forum app so as to display the users recent comments, threads they have started, and allow other users to post comments on their profile. <br>
<br>
<br>
Important Views:<br>
Profile: This view will return a profile page corresponding either to the currently logged in user, or to an imputed username should a profile with that username exist.<br>
Search_profiles: This view is not currently active in the project, but will require a simple change to allow the user to search through existing profiles. <br>
Edit_profile: This allows the signed in user to edit their profile. <br>
<br>
Models: <br>
Profile: This model represents a profile that belongs to a unique user. <br>
user: This will hold the user the profile belongs too<br>
profile_picture: This will hold the profile picture of the user<br>
personal_info: This will hold the personal info of the user<br>
firstName: This will hold the first name of the user<br>
lastName: This will hold the last name of the user<br>
displayName: This will hold a boolean to tell us if the user wants us to display their name<br>
email: This will hold the email of the user<br>
displayEmail: This will hold a boolean to tell us if the user wants us to display their email<br>
phoneNumber: This will hold the phone number of the user<br>
displayNumber: This will hold a boolean to tell us if the user wants us to display their phone number<br>
__str__: This will return the username of the user<br>
ProfileComment: This represents a comment on a specific users profile. <br>
profile: the profile the comment is on<br>
user: the user who created the comment<br>
content: the content of the comment<br>
created_at: the time the comment was created<br>
__str__: this will return a string that holds the username, and the profile username<br>

Signals:<br>
newUser: This signal will activate when a new user is registered, and will create a profile for that user.<br>

_______________________________
[SOURCES](Installation_and_deployment_guide.pdf)

<br>

CONTRIBUTERS
<br>
-Wes: Forum, Profile app, navbar<br>
-Bilge: Deployment, IdeaBoard-Item-Labels, IdeaBoard-SongRecommendation-Spotify-API, Product-Idea<br>
-Nate: IdeaBoards, storing changes locally on board till save button is pressed, adding editing deleteing items and boards, modal system to view notes<br>
<br>
[UML](SoftwareEngineering3UML.png)<br>
[System architecture](MediaBookSystemarchitecture.png)


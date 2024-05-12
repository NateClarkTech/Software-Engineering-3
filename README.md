# Software-Engineering-3
Introduction to the app: MediaBook is a platform to organize ideas for multimedia projects and connect with other creators. MediaBook has IdeaBoards where the user can create a board based on whatever project idea or topic they have. The user can then add and manage notes on the board to keep track of ideas for the project.  Notes can also have attached images and audio to allow users to keep track of sources of inspiration for their project. MediaBook also allows users to connect with other content creators and share ideas, tips, and give each other support through a user forum.



IdeaBoards App: -Bilge -Nate
	The IdeaBoards app exists to allow users to create idea or project boards to organize notes and ideas. Users can create boards for a desired topic and store notes on the boards.
The notes can contain image and sound files, text, and be labeled for sorting purposes. Users are also able to edit and delete items allowing for full user control on the content of a board.  Users can set a privacy setting for the board allowing others to see their project board.

Views:
IdeaBoard_Home: Requires use to be logged in else the user will be sent to the landing
page.  Shows the logged in user all the boards they own and allows the creation 
of new boards.
IdeaBoard_Details: Shows the user a board based on id.
	If the user is ower of the board the user can add, edit, delete items on the board.  	The user can also edit the board’s name, description, and privacy settings.
	The user can click on items on the board to see all the attached content
	If the user is not the owner but the board is public the user can look at all of the
	items on the board and sort items by label.
	
	The view also handled all add, edit, delete requests that effect the database.

Helper functions in the ideaboard views
handle_database_changes: Redirects all changes for the board to the proper functions
Handle_delete_request: Handles a board delete request from the ower of a board
add_item_to_board: Adds a new board item to the board with the content the user wants
	to add to the item
edit_item_on_board: Edits a given existing item in the database with new details using a
	given item id
delete_item_on_board: deletes an item from the database based on the item id given
edit_board_details: changes the title, description, and privacy settings of a given board
	based on id
add_label_to_database: adds a new label on a given board to the database based on
	the details given by the user

Models
IdeaBoard -Bilge -Nate
Title: title of the board (max 64 char)
description: description text for the board (max 128 characters)
is_public: privacy setting of the board (True = public, False = private)
created_at: time board was created
updated_at: time board was last edited
user: points to the user who owns the board
ItemLabel -Bilge
label_name: name of a label (max 15 characters)
label_board: board the label is on
IdeaBoardItem
title: title of the item (max 64 characters) 
description: description of the item (optional)
item_image: attached image file of the item (optional) 
image_sound: attached sound file of the item (optional)
note_label: attached label of the item (optional)
created_at: time item was created
updated_at: time item was last edited
owner: user who owns the item/board item is on
ideaboard: the board the item is on
Forms
NewIdeaBoardForm: Create new idea boards
NewIdeaBoardItemForm: Create new items for the board
NewItemLabelForm: Create new labels

API/Spotify -Bilge
Gets song recommendations


Forum app: -Wes

	The forum app exists in order to allow users of our program to interact with one another in a forum like environment. In it, users are able to create threads, post comments, subscribe to threads, receive notifications, and more. 

	Note, The forum app relies on the profile app, and will require modification to be usable on its own. 

Important views:
Forum_home: The home page of the forum, This will display the top 5 most recent threads, the top 5 most commented threads, and the top 10 most recent commenters
Thread_List: This view represents a list of threads that belong to a page. It will display the threads in a simple list. 
create_thread : View to allow a user to create a new thread, it will take in a page_id, and will create a new thread on that page
Thread_detail: This view is a detailed view of a specific view, It can take in a thread_id, and a comment_id, and will display the thread, and the comments on that thread
Create_comment: This view will allow the user to create a new comment on the forum. 
Edit_comment: This view will allow the user, or a superuser, to edit their comment. 
Delete_comment: This view will allow the user, or a super user to delete their comment. 
Like_comment: This view allows the user to like or unlike a comment not belonging to themselves. 
Reply_to_comment: This view allows the user to reply to an existing comment. 
Mark_notification_as_read: Utility view to mark a specific notification as read
Notifications_page: This view will display all of the notifications the logged in user has in a paginated list. 
Subscribe_to_thread: This view allows a user to subscribe to a thread, so that they may receive notifications on it. 
Unsubscribe_from_thread: This view allows the user to unsubscribe from the thread, and they will no longer receive notifications.


Utilities:
Convert_media_links_to_embed: Function to convert links in text to HTML IFRAME embeds for media, Currently works for youtube and spotify links
Clean_html: This function exists to attempt to remove unwanted html from the comment text. 



Models:

Page: This model will represent a single page on the thread
title: the title of the page
get_latest_comment: a method that returns the latest comment in the page

Thread:   The model that will represent a thread in the forum
page: the page the thread is on
title: the title of the thread
original_poster: the user who created the thread
subscribers: a list of users who have "subscribed" to the thread
created_at: the time the thread was created
latest_comment_time: the time of the latest comment in the thread
latest_comment_username: the username of the user who made the latest comment
comment_count: a property that returns the number of comments in the thread
Comment: The model that will represent a comment in the forum
thread: the thread the comment is on
user: the user who created the comment
content: the content of the comment
created_at: the time the comment was created
last_edited: the time the comment was last edited
likes: a list of users who have liked the comment
parent: the parent comment, if there is one, This is for the reply system
like_count: a property that returns the number of likes the comment has
Like:    The model that will represent a like on a comment
comment: the comment that was liked
user: the user who liked the comment
created_at: the time the like was created
Notification: This model will represent a notification sent to a user
notification_type: the type of notification. Can be LIKE, COMMENT, or REPLY
to_user: the user the notification is for
from_user: the user who caused the notification
thread: the thread the notification is about
comment: the comment the notification is about
date: the time the notification was created
is_read: a boolean that represents if the notification has been read



Signals
Create_comment_notification: This signal will create a notification for when a user replies to a comment



Context Processors:
Notifications: This context processor will add the global notifications to the context of every request







Profile App: -Wes, -Nate

	This app provides a user functionality for the web app. It is tightly integrated with the forum app so as to display the users recent comments, threads they have started, and allow other users to post comments on their profile. 


Important Views:
Profile: This view will return a profile page corresponding either to the currently logged in user, or to an imputed username should a profile with that username exist.
Search_profiles: This view is not currently active in the project, but will require a simple change to allow the user to search through existing profiles. 
Edit_profile: This allows the signed in user to edit their profile. 

Models: 
Profile: This model represents a profile that belongs to a unique user. 
user: This will hold the user the profile belongs too
profile_picture: This will hold the profile picture of the user
personal_info: This will hold the personal info of the user
firstName: This will hold the first name of the user
lastName: This will hold the last name of the user
displayName: This will hold a boolean to tell us if the user wants us to display their name
email: This will hold the email of the user
displayEmail: This will hold a boolean to tell us if the user wants us to display their email
phoneNumber: This will hold the phone number of the user
displayNumber: This will hold a boolean to tell us if the user wants us to display their phone number
__str__: This will return the username of the user
ProfileComment: This represents a comment on a specific users profile. 
profile: the profile the comment is on
user: the user who created the comment
content: the content of the comment
created_at: the time the comment was created
__str__: this will return a string that holds the username, and the profile username

Signals:
newUser: This signal will activate when a new user is registered, and will create a profile for that user. 


_______________________________
[SOURCES](Installation_and_deployment_guide.pdf)



CONTRIBUTERS

-Wes: Forum, Profile app, navbar
-Bilge: Deployment, IdeaBoard-Item-Labels, IdeaBoard-SongRecommendation-Spotify-API, Product-Idea
-Nate: IdeaBoards, Method for sending data to server, Local changes on boards

[UML](SoftwareEngineering3UML.png)
[System architecture](MediaBookSystemarchitecture.png)


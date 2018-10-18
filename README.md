Python version: 3.6
Django version: 2.1

Comment and post-update functions:
1. user can add comments to anywhere posts are displayed, adding comment will not refresh the page, comments from other users will not be updated before refreshing
2. the global stream will update every five seconds for new posts
3. add post and comments are both realized by jquery ajax

Follower Stream:
1. The follow and unfollow button is in the profile page. Clicking will direct to the follower stream page. User can also click the tab on the navigation bar to enter the follower stream.
2. Some rules set in the views: user cannot follow him/herself, or follow a user more than once, or unfollow an unfollowed user. 
3. There will always be a "unfollow" button on the user's own profile page, click on it will not change any relationship.

Change password through email link:
1. in the login page, click on the "forget password", follow the steps and set the new password
2. when logged in, user can change password in the profile page, a tab "change password" is added on the navigation bar

Edit Profile:
User can edit first name, last name, age and bio in the profile. If first name or last name is not specified, the value entered in the registration will be displayed.
User can upload images to profile. The profile photo will display in the profile and with the posts.


Some users been created:
paul
bob
goku
gohan
gotian
trunks

every password is "123"
the email is "username" + "@email"
Homework 4 Feedback
==================

Commit graded: 89ecb6277ecde653aa63f7c3401f65f8cbfe4b18

### Incremental development using Git (5/10)
-3, Your commit messages should be more detailed.
For example a commit with message 'grumblr' doesnt tell me anything
-2, Only files necessary for your homework solution only should be
 committed.  Files like .DS_Store are not necessary.  Ideally you should commit only source files, not derived files, to your version control repository.  If you find yourself accidentally committing derived files to your repository you should probably add the appropriate file types to your .gitignore file.
 See [https://help.github.com/articles/ignoring-files/] for details.

### Fulfilling the grumblr specification (29/30)
-1, You should only show the follow button for users you are not following, and the unfollow button for users you are following.

### Proper Form-based validation (17/20)
-3, Validation for all inputs should be done with Django Forms.
In add_post you are still manually validating input.

### Appropriate use of web application technologies (54/60)

#### Template Inheritance and Reverse Urls (10/10)

#### Image upload (5/5)

#### Email Sending (5/5)

#### Basic ORM Usage (19/20)
-1, You do not need an additional field for first name and last name since that is already stored in the Django authentication `User` model you are using.

#### Advanced ORM Usage (5/10)
-2, For following, it's not necessary to make a separate model for that relation unless you want to attach additional information to that relation. Instead, a better relation to use would be the [Many-to-many relationships](https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_many/).
-3, Instead of looping through all followed users and querying for each one, you should take advantage of Django QuerySet filtering.

#### Routing and Requests (10/10)

### Design

### Additional Information

---
#### Total score (105/120)
---
Graded by: Michael Chang (machang@andrew.cmu.edu, machang)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/zhaoc2
/blob/master/grades/homework4.md


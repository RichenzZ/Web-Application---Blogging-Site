Homework 3 Feedback
==================

Commit graded: dcc29fb4f7a26dbdf474b87aee77623fab79bb76


### Incremental development using Git (5/10)
* -5, Ideally you should create separate commits (with detailed commit messages) for each independent change you make as you work. For example, instead of committing once when you finish the assignment, you should commit after each view you implement.

### Fulfilling the grumblr specification (20/20)

### Proper input validation (20/20)

### Request routing and configuration in Django (10/10)
* -0.1, You should modularize your Django projects by using application-specific `urls.py` files in each application directory, and use your project-wide `urls.py` file to include each application's routes.

### Appropriate use of web application technologies in the Django framework (37/40)
* -2, Your call to `<Model>.objects.get()` returned 0 instances on input 6123, resulting in a `ObjectDoesNotExist` exception. You should consider returning a reasonable error message to the user.
* -1, The login page should not be shown for logged-in users. Consider redirecting them.

### Additional Information

---

#### Total score (92/100)

---

Graded by: David Yang (dzy@andrew.cmu.edu, dzy)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/zhaoc2/blob/master/grades/homework3.md


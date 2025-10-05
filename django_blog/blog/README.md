## BLOGGING PLATFORM PROJECT

# Auth setup:
    Database Configuration
        - Created a database in my local mysql using the command: CREATE DATABASE django_blog;
        - Changed the settings.py file to have mysql as the db instead of the defauly dbsqlite3
        - Implemented the Name, User, Password, Host, and Port of the mysql database
        - Installed mysqlclient using: pip install mysqlclient;
        - Tested the db by running migrations
        - Checked: USE django_blog; SHOW TABLES;
    Registration and Login
        - Created a forms.py file and implemented CustomUserCreationForm that inherits from UserCreationForm
        - Overrode UserCreationForm to issue the email field during signup
        - Implemented register and login views in views.py
        - Created auth templates at templates/blog to render the auth forms i.e CustomUserCreationForm and         Authentication Form
        - Tested and worked
✅ Successfully tested Auth by registering Waridi and Login her in using the same auth credentials

# Profile Management
- Added the LOGIN_URL = "/blogs/profile/" to show the page that unauthenticated users will be directed to if they try to access a @login_required pages
- Created a Profile model with user(OnetoOne field with the User Model) - this ensure thats one user has one corresponding profile instance. Also added phone number, bio and profile_photo.
- In forms.py created, UserInfoForm and ProfileInfoForm, to handle profile.
- Created the profile view, incorporating both forms as per the request.method. 
- Installed pillow and added media files in settings.py to handle profile_photo uploads.
- In urls.py(project-level), if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    for serving user uploads in development

# POST CRUD OPERATIONS
    - Ensure the Post model and User Models are corrently set up.
    - First, created the ListView and DetailView. All they need is to pass the queryset for the model, the template name and an optional context_object_name. They are visible to everyone, whether authenticated or not
    - Created a PostCreateForm in forms.py. The form inherits from the ModelForm base class, using Post as the model. It displays the fields, and lists the customizations for the widgets and labels. It also puts in validation checks for the title and content length.
    - Created the CreateView in views.py. Instead of passing the fields for form auto-generation, passed on the form_class, success_url(using reverse_lazy()), and template_name. Added the LoginRequiredMixin. Implemented the form_isvalid method to automatically ensure that the author is the currently authenticated user.
    - Created a blog/post_form.html to render the PostCreateForm. 
    - Created the UpdateView to handle post updates. Here the UserPassesTestMixin is added to validate that the currently authenticated user is the author of the post. It is run first hand using the test_func method. If the test_func method returns true, then the user is given access to update. If not, then the handle_no_permission is executed.
    - The same is done in the DeleteView only that an admin staff is also given access alongside the author, to delete the post.
    - The templates can be found in blog/templates/blog
    - The urls are correctly mapped.
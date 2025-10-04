Implemented Authentication using django's built-in auth.

Auth setup:
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

Profile Management
- Added the LOGIN_URL = "/blogs/profile/" to show the page that unauthenticated users will be directed to if they try to access a @login_required pages
- Created a Profile model with user(OnetoOne field with the User Model) - this ensure thats one user has one corresponding profile instance. Also added phone number, bio and profile_photo.
- In forms.py created, UserInfoForm and ProfileInfoForm, to handle profile.
- Created the profile view, incorporating both forms as per the request.method. 
- Installed pillow and added media files in settings.py to handle profile_photo uploads.
- In urls.py(project-level), if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    for serving user uploads in development


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




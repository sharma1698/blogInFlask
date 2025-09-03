Error 1:
* flask db init
* Ignoring a call to 'app.run()' that would block the current 'flask' CLI command.
   Only call 'app.run()' in an 'if __name__ == "__main__"' guard.

Ans: Flask CLI (like flask db init, flask run, etc.) loads your app from main.py, and it doesn't want app.run() to execute automatically.
Wrapping it in if __name__ == "__main__": ensures it only runs when you run the file directly, not when Flask imports it.

Error2:
ImportError: cannot import name 'db' from partially initialized module 'models' (most likely due to a circular import) (c:\Users\shank\Desktop\PycharmProjects\blogInFlask\models\__init__.py)

Ans: means you're running into a circular import issue — where two files are trying to import each other at the same time, which causes confusion during initialization.
example define ( from .contact import Contact  # ❌ this causes circular import   ) in models/__init__.py
You’re importing Contact too early inside models/__init__.py, but Contact is already trying to import db from models.

Error3:
RuntimeError: A secret key is required to use CSRF.

Answer: import os
class Config:
    SECRET_KEY = os.urandom(24)  # Generates a random secret key
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


Error4: Exception: Install 'email_validator' for email validation support.

Answer: pip install flask flask-wtf email_validator
Email() validator in WTForms → calls email_validator to check:
Proper email format (user@example.com)
Unicode and internationalized addresses
Optional DNS checking for domain


Error5: jinja2.exceptions.UndefinedError: 'form' is undefined
   pass form to :    return render_template('contact.html',form=form)

Error6: TypeError: expected string or bytes-like object, got 'int'
Answer:  the issue is that Regexp validator in WTForms expects the field’s data to be a string,
but you’re using IntegerField, which gives an int.
Use StringField + Regexp if you want to allow things like +91 or formatted numbers later.

Error7: sqlalchemy.orm.exc.UnmappedInstanceError: Class 'contact.Contact' is not mapped
Answer: The reason you still got the UnmappedInstanceError earlier is because you were trying to use the FlaskForm class named Contact in db.session.add() instead of this model.
Since both were named Contact, Python used the form class, not the model class — and SQLAlchemy complained because that class is not mapped to the database.
How to Fix
Rename one of them so that there’s no name clash.
Keep:
Contact (model) → for DB operations
ContactForm (form) → for form validation


Error8: SMTPRecipientsRefused
answer: means the mail server rejected the recipient’s email address. The email address only in angled brackets, with no name outside  eg: <john@example.com>
When you see an error like SMTPRecipientsRefused combined with a message referencing the link "https://support.google.com/a/answer/3221692", it's pointing to an underlying issue with the SMTP transaction—most likely a format or syntax problem in your email headers.


Error9: filename = secure_filename(form.img_file.data.filename)
AttributeError: 'str' object has no attribute 'filename'

answer: you are trying to access .filename on the img_file.data field even when no file has been uploaded.
  checked by this  : if hasattr(form.img_file.data, 'filename') and form.img_file.data.filename:


Error10: TypeError: normalize() argument 2 must be str, not FileStorage
Answer: The TypeError: normalize() argument 2 must be str, not FileStorage error means you're trying to pass a file object to a function that expects a string.
   -This error typically happens when you try to use a function like secure_filename() on the FileField's data directly.
   form.img_file.data.filename is the filename string. This is the text that the normalize() or secure_filename() function needs.

Error9 : Command 'pkg-config --exists mysqlclient' returned non-zero exit status 1.
         RUN pip install --no-cache-dir -r requirements.txt
         ERROR: failed to build: failed to solve: process "/bin/sh -c pip install --no-cache-dir -r requirements.txt" did not complete successfully: exit code: 1

Answer : docker build --progress=plain --no-cache -t testingBlog .
         here , --progress=plain : You get a standard, linear output, with each build step and its output printed one after the other. used for debugging
         - non-plain:It's great for visual monitoring, but can be hard to read if you need to inspect logs

         no-cache : you're starting with a completely fresh environment.

Error10 : The error ssl.SSLError: [SSL] record layer failure means that the pip command is failing to establish a secure connection to download the packages.
answer :  so added this line in Dockerfile
    # The 'ca-certificates' package is crucial for a secure network connection.
    ca-certificates \


Error11 : The TimeoutError: The read operation timed out
answer :  Unlike the previous SSL error, which was about a failed secure connection, this error means that a connection was successfully made, but the data transfer was too slow and took longer than pip's default timeout setting. This is common on slow or unstable network connections.

Add : --default-timeout 100  in  command below
RUN pip install --no-cache-dir --default-timeout 100 -r requirements.txt


Error12 : docker run -it -p 8000:5000  testing-blog
docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: exec: "gunicorn": executable file not found in $PATH: unknown

answer : gunicorn should be installed either in requirements.txt file or you can mention in Dockerfile : like
            RUN pip install gunicorn --no-cache-dir
         i have used Dockerfile to mention gunicorn , because it is not used in local


Error13 : when docker compose up --build : it gives error ImportError: libmariadb.so.3: cannot open shared object file: No such file or directory

answer : This typically happens when the Python mysqlclient library, which was successfully compiled, tries to link to its underlying C library (libmariadb.so.3) at runtime, but that shared library isn't present in the final, lean Docker image.The default-libmysqlclient-dev package we installed in the builder stage provides the development files needed for mysqlclient to compile. However, the final runner stage, which is also based on a slim image, often doesn't include the runtime shared libraries by default.To fix this, we need to explicitly install libmariadb3 in the runner stage.

      mention in Dockerfile :   libmariadb3 \
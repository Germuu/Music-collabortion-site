# PROGRESS

## Version 1

Tried to get Fly to work without success.
I was also unable to use "getenv," and thus had to hardcode the secret key and URI into the app.py file.
The site has main functionalities such as login, register, group creation, and project creation.
The project page itself is displayed when clicked, but the file-sharing functionality has not yet been implemented.

## Version 1.1

- Improved aesthetics
- Debugged group display issues
- Edited SQL schema
- Added template for displaying most recent file uploads
- While uploaded files are visible on the site, they are not yet downloadable
- secret key and URL are still hard coded

# HOW TO TEST

0. Download templates, requirements, schema.sql, and app.py.
1. Create the SQL schema using the schema.sql file.
2. Activate the virtual environment and install the requirements.
3. Run `flask run`.





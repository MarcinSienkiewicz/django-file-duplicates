# Duplicated files search using Python and Django

### About ###
The app searches recursively two paths specified by the user and lists duplicated files. The user is also given the option to delete duplicates.
Because the search is recursive, one path can't be a subdirectory of another.

#### Reading app output ####
Yellow file names in the results are the path from the **second** directory name provided by the user and, if the user chooses to, those will be the files that will get deleted.

`sha256` used for file comparison.
*Note: If the folders contain GBs of data, the search might take a while (working on one thread).*

#### Example ####
- **First path**: D:\Photos
- **Second path**: D:\Backup\Holiday photos

In this scenario, should any duplicates be found and should the user decides to delete them, the folder for deletion would be `D:\Backup\Holiday phots` so **the second** path specified by the user. This is always the case, the app will always delete duplicates from the second location specified.

#### Why Django? ####
For the sake of an easy-to-make GUI, the aim of this app wasn't to make it a 'proper' website. Intended to be run locally on:
`localhost:<port_number>` or `127.0.0.1:<port_number>`
usually:
`127.0.0.1:8000`

## How to run on Windows ##
Step-by-step commands while being on **D:\\**  drive.

Have specified the full path while issuing commands for clarity. Syntax used:
<path_you're_in>`command`



**1. Create a virtual environment:**

D:\\>`python -m venv my_new_env`

**2. Activate environment:**

D:\\>`cd my_new_env\Scripts`

D:\\>my_new_env\\Scripts>`activate.bat`

(my_new_env) D:\\>my_new_env\\Scripts>`cd..`

(my_new_env) D:\\>my_new_env>

**3. Clone the project (you are in your my_new_env dir)**

(my_new_env) D:\\>my_new_env>`git clone https://github.com/MarcinSienkiewicz/django-file-duplicates.git`

**4. cd into project and install the requirements**

(my_new_env) D:\\>my_new_env>`cd django-file-duplicates`

(my_new_env) D:\\>my_new_env\\cd django-file-duplicates> `pip install -r requirements.txt`

**5. Start local server to use the project**

(my_new_env) D:\\>my_new_env\\cd django-file-duplicates>`python manage.py runserver`

**6. Open the project in your web browser by typing in the URL bar result of step 5, usually:**

`127.0.0.1:8000`
# Cinematography_Rater
The idea behind the app is that users can receive ratings for their “posts” based on the cinematic quality of the post's content, Each post contains a single image and text-based information, such as the location where the photo was taken and details about the shooting conditions, including the lens or camera settings.

In the app:
- Users can create an account and log in to the app.
- Users can add “posts” to the app. Additionally, users can edit and delete the “posts” they have added.
- Users can view “posts” added to the app. Users can see both the “posts” they have added themselves and those added by other users.
- Users can search for “posts” by keyword or other criteria. Users can search for both the “posts” they have added themselves and those added by other users.
- The app includes user profiles that display statistics for each user and the “posts” they have added.
- Data items can be assigned multiple categories, which are stored in the database. For each category, the user can select one option from several available choices.
- In addition to the main “posts,” the app includes comments. Users can add comments related to their own “posts” and those of other users.

# How to test software
1. Clone the repository:
   ```python
   git clone https://github.com/OliverLaaksoHY/Cinematography_Rater
   ```
3. Navigate to the project directory:
   ```python
   cd Cinematography_Rater
   ```
5. Activate the virtual environment:
   ```python
   source venv/bin/activate
   ```
6. Create a database

      a) Create database
      ```sh
      touch database.db
      ```
      b) Open sqlite3
      ```python
      sqlite3
      ```
      c) Open database file in sqlite3
      ```python
      .open database.db
      ```
      d) Add the required database tables by copying the contents of the file schema.sql into the terminal that is running sqlite3 
      e) Quit sqlite3
         ```python
      .quit
      ```
8. Start the Flask application: 
   ```python
   flask run
   ```
9. Open address shown in the terminal in a web browser such as Chrome or Firefox 

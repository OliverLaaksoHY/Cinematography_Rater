# Cinematography_Rater
The idea behind the app is that users can receive ratings for their images based on the cinematic quality aka cinematography of the image. Each post contains a single image and text-based information regarding it, such as the location where the photo was taken and focal length.

In the app:
- Users can create an account and log in to the app.
- Users can post images to the app. Additionally, users can edit and delete the images they have added.
- Users can view images added to the app. Users can see both the images they have added themselves and those added by other users.
- Users can search for images by keyword or other criteria. Users can search for both the images they have added themselves and those added by other users.
- The app includes user profiles that display statistics for each user and the images they have added.
- IMages be assigned multiple categories, which are stored in the database. For each category, the user can select one option from several available choices.
- In addition to the main images, the app includes reviews. Users can add reviews related to their own “posts” and those of other users.

# Functionality with large data
Tested with seed.py file; 1 000 users, 10 000 posts and 10 000 reviews. The pages of the website loaded a bit slow, but each image could be viewed and systems like adding posts worked.  


# How to test software
1. Clone the repository:
   ```python
   git clone https://github.com/OliverLaaksoHY/Cinematography_Rater
   ```
3. Navigate to the project directory:
   ```python
   cd Cinematography_Rater
   ```
4. Create virtual environment
```
python -m venv venv
```
And activate it:  
```
source venv/bin/activate
```
6. Install flask:
   ```
   pip install flask
   ```
7. Create a database and fill the database using the command
      ```
      sqlite3 database.db < schema.sql 
      ```
      and
      ```
      sqlite3 database.db < init.sql
      ```
      in the linux cli shell.
      
8. Start the Flask application: 
   ```python
   flask run
   ```
9. Open address shown in the terminal in a web browser such as Chrome or Firefox 

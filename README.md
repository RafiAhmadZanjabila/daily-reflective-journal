# Daily Reflective Journal
The Daily Reflective Journal is a web application designed to help users track their habits, moods and diary entries. This project provides a user-friendly platform for personal growth and self-awareness.

## Distinctiveness and Complexity
The **Daily Reflective Journal** is a web application that distinguishes itself from the other projects in this course by combining features generally found in separate applications: mood tracking, habit tracking and diary entries into a single application. Unlike other journaling tools, this application focuses not only on documenting daily events but also on emotional and behavioral self awareness by helping users identify patterns in their moods and habits over time and write about their day in the diary. This integration of features makes the application highly distinctive, as it is not limited to just one purpose, like logging activities or creating posts, but instead offers a holistic tool for personal growth.

One of the aspect of this project's distinctiveness is its dual focus on emotional well being and productivity. The mood tracking component allows users to select and log their daily emotional state, providing insights into their mental health trends. This feature is complemented by the habit tracker, which encourages users to monitor their progress toward specific goals, for consistency and discipline. Writing diary entries helps to keep track of their daily life. While other projects in the course, such as Auctions or Twitter, focus on commerce or social networking, this project promotes introspection and personal development, which is a complete different category. Furthermore, the integration of all these features under one application, along with user friendly navigation and a responsive design, sets it apart from standard journaling or habit tracking applications.

In terms of complexity, the application demonstrates a good level of technical integration. The backend manages the relational database that stores user data, including mood logs, habits and diary entries. Models are designed to ensure efficient data relationships, such as linking moods and habits to individual users while maintaining a strong authentication and session management. Advanced Django features like custom template filters, rest framework for apis and form handling with CSRF protection are employed.

On the frontend JavaScript is used for interactivity and the Fetch API for asynchronous operations which makes the application complex. For example, the mood tracker dynamically updates data without requiring full page reloads. Similarly, the habit tracker allows users to edit or delete tasks with immediate feedback reflected in the interface.

## Project Structure
I won't show the files provided by Django, only the ones I created or modified.

The project uses `Bootstrap`, `jQuery` and `Google Fonts`. Make sure that you are connected to the internet when running the application to load the files from the CDN.

### Main Application Files
- `reflectionjournal`: The main Django project folder.
- `reflectionjournal/urls.py`: Root URL configuration for routing requests to the appropriate app-level URLs.
- `templatetags`: Folder containing custom template tags and filters used in Django templates to add unique functionality.
- `templatetags/custom_filters.py`: Custom template filters for formatting time (minutes to words) and weather icons.

### App-Specific Files (`app`)
- `models.py`: Defines the database schema, including tables for diary entries, mood tracking and habit tracking.
- `views.py`: Contains all the logic for handling user requests and returning appropriate responses or templates.
- `urls.py`: Manages routing for the app, linking specific paths to corresponding views.
- `admin.py`: Configuration for registering models with the Django admin panel.
- `utils.py`: Contains reusable helper functions used across the application. It contains a `get_emotion_color` function that returns a color based on the user's mood selection.

### Static files
Static Folder Structure:
- `styles`: Contains CSS files for designing the application.
    - `app.css`: Home page styling.
    - `layout.css`: Shared layout styling for all pages.
    - `home.css`: Landing page styling.
    - `diary.css`, `habit.css`, `mood.css`: Custom styles for respective features.
    - `weather-icons.min.css`: Styles for weather icons used in the mood tracker.
- `scripts`: Contains JavaScript files for interactivity and front-end logic.
    - `app.js`: Homepage greeting functionality.
    - `diary.js`: Handles diary-specific interactivity.
    - `habit.js`: Handles habit tracking functionality.
    - `mood.js`: Handles mood tracking functionality.
- `assets`: Contains images used in the web application.
- `fonts`: Contains weather icons used in the mood tracker.
> The weather icons are from [Weather Icons](https://erikflowers.github.io/weather-icons/). The `weather-icons.min.css` file provides the styles for these icons and `fonts` folder contains the font files. All these required things are downloaded from the official website.

### Templates
- **General Templates**
    - `layout.html`: Base template containing the global layout structure.
    -  `home.html`: Landing page with a welcome message and overview of features.
- **Feature-Specific Templates**
    - `app.html`: Homepage of the application with mood, habit and diary tracking sections.
    - `mood_home.html`, `habit_home.html`, `diaryhome.html`: Dashboards for mood, habit tracking and diary entry showing current and past entries.
    - `add_mood.html`, `add_habit_entry.html`, `writediary.html`: Pages for adding data to respective features.
    - `mood_detail.html`, `habit_detail.html`, `diary_detail.html`: Detailed views for specific entries with options to edit and delete them.
- **Authentication Templates**
    - `login.html`: User login page.
    - `register.html`: User registration page.

### API App (`api`)
The api app is built using Django Rest Framework (DRF) to provide a RESTful API for various functionalities within the project. Currently, it includes one route that serves emotions for the mood tracking feature.
- `views.py`: Contains the logic for the API endpoints. In this case, it has a view that fetches and returns a list of predefined emotions for the mood tracking functionality in JSON format from the database.
- `serializers.py`: Defines the serializers that convert Django models or other data structures into JSON format and vice versa.
- `urls.py`: Manages the API-specific routing, mapping URLs to their corresponding views. Currently, it defines a single route that provides the emotions data for mood tracking.

## Steps to run
1. Clone the repo.
2. Change the working directory.
3. Install Dependencies:
```bash
pip install -r requirements.txt
```
4. Migrate the Database:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create a Superuser (Optional for Admin Access)
```bash
python manage.py createsuperuser
```
6. Start the development server
```bash
python manage.py runserver
```
7. Open the brower and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the application.

## Additional Information
This project helped me learn and implement something new (Django Rest Framework) and some advanced JavaScript concepts. I also learned how to make my own template filters because templating comes with its limitations and using template tags will help me give more control over the application.

I had planned to add advanced analysis to my project that performs data visualization with graphs and data insights. But because of time constraints and the complexity of the project with my own limited knowledge about implementing this, I had to drop this feature and this leaved the project with only one route in the API app which used Django REST Framework. I will definitely try to implement this in the future.
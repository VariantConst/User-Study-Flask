This project is a Flask-based web application designed for conducting image selection tasks. It allows users to log in, view a gallery of images, and select images based on specific criteria provided. The application tracks user progress and ensures that participants can only complete the task once. It's ideal for research studies or surveys where participants are asked to compare and choose images based on aesthetic, conceptual, or other criteria.

## Features

- **User Authentication**: Users can log in to start or continue their tasks.
- **Progress Tracking**: The application saves user progress in a database, allowing participants to pause and resume their tasks.
- **Image Selection**: Users select images from a gallery, with their choices being recorded for further analysis.
- **Completion Status**: Once a user has made selections across all provided images, they are directed to a completion page.

## Usage

### Prerequisites

Before running the application, ensure you have Python and Flask installed on your system. Additionally, the project relies on a SQLite database for tracking user progress and storing image selections, so ensure you have the appropriate setup for SQLite.

### Running the Application

1. **Start the Application**:
   To start the web service, navigate to the project directory in your terminal and run the following command:

   ```bash
   python app.py
   ```

   This command launches the Flask application and makes it accessible on `http://localhost:5000`.

2. **Accessing the Web Interface**:
   - Open a web browser and go to `http://localhost:5000`.

### Modifying Image Source

- To change the source or method of loading images, modify the `utils/dataset.py` file. This is where the application pulls image data for the gallery.

# Post App

Post App is a simple web application that allows users to register, create posts, like and comment on posts, and reply to comments. The app provides a platform for users to share content and engage in discussions.

## Features
- User Registration: Users can create an account to start using the app.
- Post Creation: Registered users can create and share posts with others.
- Liking Posts: Users can like posts to show their appreciation.
- Commenting on Posts: Users can leave comments on posts to engage in discussions.
- Replying to Comments: Users can reply to comments to create threaded conversations.


### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/zhenyakhachatryan/Post-App.git
    cd Post-App
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS and Linux:

      ```bash
      source venv/bin/activate
      ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up your environment variables. Create a `.env` file in the root directory and add your API key:

    ```plaintext
    FLASK_APP=app.py
    API_KEY=your_api_key_here
    ```

6. Run the application:

    ```bash
    flask run
    ```

7. Open your browser and go to `http://127.0.0.1:5000`.

## Usage

- Register a new user by clicking the "Register" button.
- Log in with your credentials.
- Create a new post by navigating to the "Create Post" section.
- Like a post by clicking the "Like" button on any post.
- Comment on a post by entering your comment in the input field and clicking "Comment".
- Reply to a comment by clicking the "Reply" button under the comment and submitting your reply.

## Technologies Used

- Python
- Flask
- Flask SQLAlchemy
- SQLite
- HTML/CSS
  
##Contact

For questions or support, please contact me at khachatryanzhenya3@gmail.com.

Thank you for using Post App!

# Activity Sharing App

## Overview
The Activity Sharing App enables users to create, share, and join activities with friends. It is built using Flask and SQLite, providing a simple, intuitive interface for spontaneous event planning. Users can register, log in, create activities, and join existing ones.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/activity-sharing-app.git
   cd activity-sharing-app
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python run.py
   ```

## Key Features
- User Registration and Login: Users can register, log in, and view their profiles.
- Create Activities: Users can create new activities with a name, description, date, and time.
- Join Activities: Users can view upcoming activities and join any activity they find interesting.
- View Activity Details: Each activity has a detailed page displaying all the relevant information.
- Profile View: Users can view the profiles of other participants, including their joined activities.
- Activity Management: Users can update or delete activities they have created.
- Role-Based Access Control: Only the creator of an activity can modify or delete it.

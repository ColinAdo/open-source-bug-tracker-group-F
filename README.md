# Open Source Issue Tracking Application Group F
    
## User Registration and Authentication: Done 
Users should be able to create accounts, log in, and log out securely. User authentication is essential to ensure that only authorized individuals can access and modify the issue-tracking system.

## Issue Tracking and Management: 
The core functionality of the application is to track and manage issues in open-source repositories. Users should be able to create, view, edit, and close issues. Each issue typically includes information such as a title, description, issue type, severity, status, and comments.

## Categorization and Filtering: 
Issues should be categorizable by type (e.g., bug, feature, enhancement), severity (e.g., critical, major, minor), and status (e.g., open, in progress, closed). Users should be able to filter issues based on these categories.

## Search Functionality: 
We need to implement a search feature that allows users to search for specific issues based on keywords, issue numbers, or other relevant criteria.

## Commenting and Discussion: 
Users should be able to add comments to issues, enabling discussions and collaboration among team members or contributors.

## User Roles and Permissions: 
We need to define user roles with varying levels of permissions. Common roles might include administrators, developers, and viewers. Admins may have full control, developers can create and modify issues, and viewers can only read issues.

## Security Measures:     
We need to implement security features to protect the application and data. This includes secure user authentication, authorization, and data encryption to prevent unauthorized access and data breaches.

##  Performance Optimization: 
We need to ensure the application is responsive and can handle a significant number of issues and users.

## Data Backup and Recovery: 
Regularly back up issue data to prevent data loss in case of system failures or data corruption.

##  User Interface (UI) Design: 
We need to design an intuitive and user-friendly interface to make it easy for users to navigate and interact with the application.

## Testing: 
Follow a testing plan to ensure the application's functionality, security, and performance meet the specified requirements.

## Conventions: 
Please create a branch using your student name i.e Bsclmr00001
Locate your flask_login/utils.py that is:
/path/to/your/virtualenv/lib/python3.10/site-packages/flask_login/utils.py.

Remove this imports: 
* **from werkzeug.urls import url_decode**
* **from werkzeug.urls import endecode and the paste this code;**

**And add this imports** 
* **from werkzeug.datastructures import MultiDict**
* **from urllib.parse import urlencode**

**Rename the url_decode function in the file to MultiDict**
**Rename urlencode function in the file to urlencode and then remove sort=True argument from the urlencode.**

**To Run the application locally**
Run: 
* **Cone the code**
* **pip install requirements.txt**
* **export FLASK_APP=application.py**
* **flask run --debug # For debug mode**

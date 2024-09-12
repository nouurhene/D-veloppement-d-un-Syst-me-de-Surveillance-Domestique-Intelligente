# Smart Home Surveillance System with Facial Recognition and Email Security

## Overview

This project is a **Smart Home Surveillance System** that integrates **facial recognition** with **email-based security verification**. It monitors and identifies individuals using facial recognition and, when an unknown face is detected, captures an image and sends a notification email to the system administrator. The system also includes a user registration process secured by email verification.

## Features

- **Facial Recognition**: Detects and recognizes faces using a pre-trained model.
- **Email Notifications**: Sends an email alert with a photo of any unrecognized person.
- **User Registration**: Allows new users to register, with a confirmation code sent via email for validation.
- **Video Recording**: Records and stores surveillance footage in a dedicated directory, with each video named by date.
- **Camera Control**: The user can activate and deactivate the camera from the Qt interface.
- **User Management**: Add or remove users directly through the GUI.

## Technologies Used

- **Programming Languages**: Python
- **Frameworks & Libraries**:
  - PyQt5 (for the GUI)
  - SQLite (for user management)
  - OpenCV & dlib (for facial recognition)
  - smtplib (for email notifications)
- **Tools**: Qt Designer (for designing the GUI)
  
## Installation

### Prerequisites

- Python 3.x
- Virtual environment tools (`venv`)
- Required Python libraries (`PyQt5`, `OpenCV`, `dlib`, `smtplib`)

### Step-by-Step Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/surveillance-system.git
   cd surveillance-system
2. **Create a virtual environment:**
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
3.**Install the dependencies:**
   pip install -r requirements.txt

##Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your-email@gmail.com'
EMAIL_PASSWORD = 'your-email-password'
RECIPIENT_EMAIL = 'recipient-email@gmail.com'

##Contact
For any questions or collaboration inquiries, feel free to reach out:

Name: Kouki Nourhene
Email: koukinourhen03@gmail.com


# Society Management System

## Overview

The Society Management System is a Django-based web application designed to manage transactions and user information for a society. It utilizes Firebase for user authentication and data storage.

## Features

- Admin dashboard to manage transactions and view user data
- User management with the ability to toggle active status and update pending amounts
- Transaction logging with pagination
- Firebase integration for user authentication and data storage

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/society-management-system.git
    cd society-management-system
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Firebase:**

    - Create a Firebase project and obtain your service account key JSON file.
    - Set the Firebase credentials as an environment variable:

      ```bash
      export GOOGLE_CLOUD_SERVICE_ACCOUNT='{"type":"service_account","project_id":"your-project-id", ...}'
      ```

5. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Visit `http://127.0.0.1:8000` in your browser to access the application.**

## Usage

- **Admin Dashboard:**
  - Manage transactions.
  - View and update user data.

- **User Management:**
  - Admins can toggle user activation status and update pending amounts.

- **Transaction Log:**
  - View recent transactions with pagination.

## Deployment

To deploy this project on Vercel:

1. **Install Vercel CLI:**

    ```bash
    npm install -g vercel
    ```

2. **Log in to Vercel:**

    ```bash
    vercel login
    ```

3. **Deploy the project:**

    ```bash
    vercel --prod
    ```

4. **Configure environment variables on Vercel:**
   - Add the `GOOGLE_CLOUD_SERVICE_ACCOUNT` environment variable with the JSON credentials.

## Notes

- Ensure sensitive files, such as the Firebase service account key, are not pushed to the repository.
- Use GitHub Secrets or similar services for managing sensitive information.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Firebase for authentication and data storage.
- Django for the web framework.

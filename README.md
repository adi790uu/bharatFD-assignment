# FAQ Management System

## Overview

The FAQ Management System is a web application built using FastAPI that allows users to create, retrieve, and delete FAQs in multiple languages. The application supports caching with Redis and provides a user-friendly interface for both administrators and users.

## Features

- Create FAQs with questions and answers in multiple languages.
- Retrieve FAQs based on selected language.
- Delete FAQs.
- Admin interface for managing FAQs.
- User interface for viewing FAQs.

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python.
- **SQLAlchemy**: ORM for database interactions.
- **Redis**: In-memory data structure store for caching.
- **Pydantic**: Data validation and settings management.
- **HTML/CSS/JavaScript**: Frontend technologies for the user interface.

## Installation

### Prerequisites

- Python 3.7 or higher
- PostgreSQL or any other supported database
- Redis server

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/faq-management-system.git
   cd faq-management-system
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables. Create a `.env.development` file in the root directory with the following content:

   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   REDIS_URL=redis://localhost:6379/0
   TEST_DATABASE_URL=postgresql+asyncpg://user:password@localhost/test_dbname
   ```

5. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

### API Endpoints

#### 1. Create FAQ

- **Endpoint**: `POST /api/faqs/create`
- **Request Body**:
  ```json
  {
    "question": "What is FastAPI?",
    "answer": "FastAPI is a modern web framework for building APIs.",
    "language": "en"(OPTIONAL)
  }
  ```
- **Response**:
  - Status: `201 Created`
  - Body:
    ```json
    {
      "success": true,
      "message": "FAQ created successfully!",
      "data": {
        "id": 1,
        "question": "What is FastAPI?",
        "answer": "FastAPI is a modern web framework for building APIs."
      }
    }
    ```

#### 2. Get FAQs

- **Endpoint**: `GET /api/faqs/`
- **Query Parameters**: `lang` (default: `en`)
- **Response**:
  - Status: `200 OK`
  - Body:
    ```json
    {
      "success": true,
      "message": "Faqs fetched successfully!",
      "data": {
        "faqs": [
          {
            "id": 1,
            "question": "What is FastAPI?",
            "answer": "FastAPI is a modern web framework for building APIs."
          }
        ]
      }
    }
    ```

#### 3. Delete FAQ

- **Endpoint**: `DELETE /api/faqs/delete`
- **Query Parameters**: `faq_id`
- **Response**:
  - Status: `200 OK`
  - Body:
    ```json
    {
      "success": true,
      "message": "Faq deleted successfully!"
    }
    ```

### Frontend

The application includes a simple frontend for both admin and user interfaces:

- **Admin Page**: Allows administrators to create and manage FAQs, You can access it at /admin.
- **User Page**: Allows users to view FAQs based on selected language, You can access it at /user.

### Running Tests

To run the tests, use the following command:

```bash
   pytest tests/
```

## Screenshots

### Admin Section Screenshots:

_Multilingual support._

![Admin Page](screenshots/admin_1.png)

![Admin Page](screenshots/admin_2.png)

### User Section Screenshots:

_User can select the language and faqs will be displayed._

![User Page](screenshots/user_1.png)
![User Page](screenshots/user_2.png)

## Optimizations

#### Translation method:

The translation service has been optimized for better performance and efficiency. Key improvements include:

- **Asynchronous Processing**: The `translate_text` function now uses `asyncio.gather()` to translate FAQs into multiple languages concurrently. This reduces the overall time required for translations, enhancing the responsiveness of the application.

- **Batch Database Operations**: Translations are collected in a list and inserted into the database in a single operation. This minimizes the number of database interactions, improving performance and reducing latency.

- **Robust Error Handling**: The function includes comprehensive error handling to log any issues that arise during the translation process, ensuring that the application remains stable and user-friendly.

These optimizations contribute to a more efficient and responsive FAQ management system, providing users with quick access to translated content.

#### Caching

The FAQ Management System employs a caching strategy using Redis to enhance performance and reduce database load. Key aspects of the caching strategy include:

In-Memory Caching: FAQs are cached in Redis, allowing for quick retrieval without repeated database queries.

Cache Key Generation: Unique cache keys are generated based on the requested language (e.g., faqs:en), ensuring that FAQs for different languages are stored separately.

Cache Lookup Before Database Query: The application checks the cache for FAQs before querying the database. If the data is found in the cache, it is returned immediately, improving response times.

Cache Expiration: Cached FAQs are set to expire after a specified duration (e.g., 1 hour), preventing stale data from being served.

Cache Updates on Create/Delete: The cache is updated whenever a new FAQ is created or an existing FAQ is deleted, ensuring that users always receive the most current data.

This caching strategy significantly improves the efficiency and responsiveness of the FAQ Management System, providing users with a seamless experience.

#### Results:

- Due to asynchronous processing the time to translate the faq came down by almost 10 seconds.
- Caching also improved the response times, after the initial request which took around 3-4 seconds it came down below 1 second.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Redis](https://redis.io/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

# API Documentation

## Authentication

The API uses token-based authentication. To access protected endpoints, you need to include a valid token in the `Authorization` header of your requests.

### Obtaining a Token

You can obtain a token by sending a POST request to the `/api/token/` endpoint with your username and password.

**Request:**

```bash
curl -X POST -d "username=<your_username>&password=<your_password>" http://127.0.0.1:8000/api/token/

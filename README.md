# Healthcare API Project

A Django REST API for managing patient records and heart rate monitoring.

## Features

- User Authentication (Register/Login)
- Patient Management (CRUD operations)
- Heart Rate Monitoring
- Filtering and Pagination
- Data Validation
- Error Handling

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/yourusername/healthcare-api.git
cd healthcare-api
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

## API Documentation

### Authentication Endpoints

#### 1. Register User
- **URL**: `POST /api/register/`
- **Body**:

```json
{
"email": "user@example.com",
"password": "password123"
}
```

#### 2. Login
- **URL**: `POST /api/login/`
- **Body**:

```json
{
"email": "user@example.com",
"password": "password123"
}
```

## Patient Endpoints

### 1. Create Patient
- **URL**: `POST /api/patients/`
- **Body**:

```json
{
"first_name": "John",
"last_name": "Doe",
"date_of_birth": "1990-01-01",
"gender": "M",
"contact_number": "1234567890",
"address": "123 Main St"
}
```

### 2. Get Patients
- **URL**: `GET /api/patients/`
- **Query Parameters**:
  - `first_name`
  - `last_name`
  - `gender`
  - `page`

## Heart Rate Endpoints

### 1. Create Heart Rate Record
- **URL**: `POST /api/heart-rates/`
- **Body**:

```json
{
"patient": 1,
"heart_rate": 75,
"recorded_at": "2024-02-18T10:00:00Z",
"notes": "Regular checkup"
}

### 2. Get Heart Rate Records
- **URL**: `GET /api/heart-rates/`
- **Query Parameters**:
  - `patient_id`
  - `heart_rate_min`
  - `heart_rate_max`
  - `recorded_at_after`
  - `recorded_at_before`
  - `page`

## Data Models

### User
- email (unique)
- username
- password
- first_name
- last_name

### Patient
- first_name
- last_name
- date_of_birth
- gender (M/F/O)
- contact_number
- address

### Heart Rate Record
- patient (Foreign Key)
- heart_rate (0-300)
- recorded_at
- notes (optional)

## Assumptions and Design Decisions

1. Authentication:
   - Email-based authentication implemented
   - CSRF protection disabled for API endpoints
   - Session-based authentication used for simplicity

2. Data Validation:
   - Phone numbers must be numeric
   - Heart rate values between 0-300
   - Date of birth cannot be in the future

3. API Design:
   - RESTful architecture
   - Pagination (10 items per page)
   - Filtering capabilities for both patients and heart rates
   - Error handling middleware

4. Security:
   - Basic authentication for development
   - CORS enabled for all origins in development

## Development Choices

1. Used Django REST Framework for:
   - Serialization
   - ViewSets
   - Authentication
   - Filtering

2. Implemented custom:
   - Email authentication backend
   - Error handling middleware
   - Data validation

## Production Considerations

1. Security:
   - Implement JWT authentication
   - Configure CORS for specific origins
   - Enable CSRF protection
   - Use HTTPS
   - Secure cookie settings

2. Performance:
   - Add caching
   - Database optimization
   - Rate limiting

## Testing

Run tests with:
```bash
python manage.py test
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request




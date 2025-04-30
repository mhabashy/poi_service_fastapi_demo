# POI Service API

A REST API for submitting and moderating Points of Interest (POIs) with image support. This service allows users to submit POIs which are then reviewed by moderators before being published

## Features

- Submit POIs with optional images (stored as base64) - easily change it to AWS S3 / Google Cloud Storge
- Moderation workflow (approve/reject with reasons)
- Basic API key authentication for moderators
- OpenAPI documentation
- Docker and Docker Compose for easy deployment

## Tech Stack

- **FastAPI**: Modern, high-performance web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **MySQL**: Database backend
- **Docker**: Containerization
- **JWT**: Token-based authorization for moderation actions

## API Endpoints

### Public Endpoints

- `POST /pois/`: Submit a new POI with optional image
- `GET /pois/`: Get all approved POIs
- `GET /pois/{poi_id}`: Get a specific approved POI

### Moderation Endpoints (Requires API Key)

- `GET /moderation/pois`: Get all POIs for moderation
- `GET /moderation/pois/pending`: Get pending POIs
- `POST /moderation/pois/{poi_id}/approve`: Approve a POI
- `POST /moderation/pois/{poi_id}/reject`: Reject a POI with reason
- `POST /moderation/api-keys`: Create new API keys
- `POST /moderation/api-token`: Create new Token

-- Created a new 

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Installation

1. Start the containers:
   ```bash
   docker-compose up --build
   ```

2. The API will be available at http://localhost:8000
   - API documentation: http://localhost:8000/docs

### Default API Key

A default API key is generated on first startup. Check the console logs for a message like:
```
Created default API key: xxxxxxxx
```

Use this API key in the `X-API-Key` header for authenticated endpoints.

Once you create a key you can use it to generate a token. Normally will create a user login for this part however that this good enough to show off Python FastAPI

## Development

The project is configured for hot reloading, so any changes to the code will be automatically applied. The entire project directory is mounted into the container.

## Example Usage

### Creating a POI (JSON Request)

```bash
curl -X POST "http://localhost:8000/pois/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Eiffel Tower",
    "description": "Famous landmark in Paris",
    "latitude": 48.8584,
    "longitude": 2.2945,
    "address": "Champ de Mars, 5 Av. Anatole France, 75007 Paris, France",
    "category": "landmark",
    "images": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAoHBwgHBgoICAgLCgoLDhg
QDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4ND
hwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv
/wAARCAAYACADASIAAhEBAxEB/8QAGAAAAwEBAAAAAAAAAAAAAAAAAAUHBgT/xAAmEAABAwMEAgEFA
AAAAAAAAAABAgMRAAQFBhIhQRNRMRUiMmGB/8QAGAEAAwEBAAAAAAAAAAAAAAAAAAIEAQP/xAAcEQA
CAgIDAAAAAAAAAAAAAAAAAQMxESECImH/2gAMAwEAAhEDEQA/AKGWG1n42pHFKc1cfS8eq4S0HvuCE
oKtsk+z1T+4cTLYgATHFTrUWs7bJ3qsZZ2y1tJcDT1y5MIVMSAP32aok59fTpFezS429XkLNt15pDK
kr2KSlW4cRyD65rruUqKt6Px+BWYw2p2rLLMYO4ZHkcASl1tYI3ETCgf5WslQZ8RSCCSUmtjeVsJHt
4DJXILstclLZMDs9VBlZd1u5uQpCmnLl7c7IggzJEdUUVPMqBNqhxp9x3I6+t3RthD5eM+kiq2Xt6V
SOZ4oopoqyK6P/9k="]
  }'
```

## Project Structure

```
poi_service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── poi.py
│   │   └── moderation.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
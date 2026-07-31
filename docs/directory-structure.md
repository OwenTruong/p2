spacebnb/
├── frontend/
├── services/
│   ├── auth-service/
│   ├── listing-service/
│   └── reservation-service/
├── shared/
├── infrastructure/
├── deployment/
├── monitoring/
├── docs/
├── scripts/
├── devops/
├── docker-compose.yml
└── README.md


listing-service/
├── app/
│   ├── api/
│   │   ├── controllers/
│   │   │   └── listings.py
│   │   └── dependencies.py (extracting dependency injection from routes)
│   ├── models/
│   │   └── listing.py
│   ├── dtos/
│   │   ├── listing_update.py
│   │   └── listing_create.py
│   ├── repositories/
│   │   └── listing_repository.py
│   ├── services/
│   │   └── listing_service.py
│   ├── clients/ (handle service-to-service communication)
│   │   └── reservation_client.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── logging.py
│   └── main.py
~~├── migrations/~~
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
└── README.md
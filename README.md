# Shop API - Backend Web Application

A minimalistic backend web application for an online shop built with Go, Gin framework, GORM, and SQLite.

## Features

- Full CRUD APIs for:
  - Customer (ID, Name, Surname, Email)
  - ShopItemCategory (ID, Title, Description)
  - ShopItem (ID, Title, Description, Price, Category list)
  - OrderItem (ID, ShopItem, Quantity)
  - Order (ID, Customer, Items list)
- RESTful API endpoints
- SQLite database with GORM
- Docker containerization
- Comprehensive test suite
- Auto-initialization of test data

## API Endpoints

### Customers
- `GET /api/v1/customers` - Get all customers
- `GET /api/v1/customers/:id` - Get customer by ID
- `POST /api/v1/customers` - Create new customer
- `PUT /api/v1/customers/:id` - Update customer
- `DELETE /api/v1/customers/:id` - Delete customer

### Categories
- `GET /api/v1/categories` - Get all categories
- `GET /api/v1/categories/:id` - Get category by ID
- `POST /api/v1/categories` - Create new category
- `PUT /api/v1/categories/:id` - Update category
- `DELETE /api/v1/categories/:id` - Delete category

### Shop Items
- `GET /api/v1/shopitems` - Get all shop items
- `GET /api/v1/shopitems/:id` - Get shop item by ID
- `POST /api/v1/shopitems` - Create new shop item
- `PUT /api/v1/shopitems/:id` - Update shop item
- `DELETE /api/v1/shopitems/:id` - Delete shop item

### Orders
- `GET /api/v1/orders` - Get all orders
- `GET /api/v1/orders/:id` - Get order by ID
- `POST /api/v1/orders` - Create new order
- `PUT /api/v1/orders/:id` - Update order
- `DELETE /api/v1/orders/:id` - Delete order

## Prerequisites

- Docker and Docker Compose
- Go 1.21+ (for local development)

## Setup and Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd shop-api
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8080`

### Local Development

1. Install dependencies:
```bash
go mod download
```

2. Set up SQLite database path (optional):
```bash
export DB_PATH=./shopdb.sqlite
```

3. Run the application:
```bash
go run main.go
```

## Running Tests

### Using Docker
```bash
docker-compose exec app go test ./tests/...
```

### Local Testing
```bash
go test ./tests/...
```

## Project Structure

```
shop-api/
├── config/
│   └── database.go          # Database configuration
├── handlers/
│   ├── customer.go          # Customer CRUD handlers
│   ├── category.go          # Category CRUD handlers
│   ├── shopitem.go          # Shop item CRUD handlers
│   └── order.go             # Order CRUD handlers
├── models/
│   └── models.go            # Data models and migrations
├── routes/
│   └── routes.go            # API route definitions
├── tests/
│   └── api_test.go          # API endpoint tests
├── test_collections/        # Test data files
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Docker configuration
├── go.mod                  # Go module dependencies
├── main.go                 # Application entry point
└── README.md               # This file
```

## Example API Usage

### Create a Customer
```bash
curl -X POST http://localhost:8080/api/v1/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"John","surname":"Doe","email":"john.doe@example.com"}'
```

### Get All Customers
```bash
curl http://localhost:8080/api/v1/customers
```

### Create a Shop Item
```bash
curl -X POST http://localhost:8080/api/v1/shopitems \
  -H "Content-Type: application/json" \
  -d '{"title":"Laptop","description":"Gaming laptop","price":1299.99}'
```

## Environment Variables

- `DB_PATH` - SQLite database file path (default: ./shopdb.sqlite)

## Test Data

The application automatically initializes with test data including:
- Sample customers (John Doe, Jane Smith)
- Sample categories (Electronics, Books)
- Sample shop items (Smartphone, Science Fiction Novel)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests to ensure they pass
6. Submit a pull request
~~~

~~~patch
type=New
path=fleet-file://lmengb9jdeaclg35ju0p/Users/booboo/air/air_1/Makefile?type=file&root=%252F
~~~
~~~makefile
.PHONY: build run test clean docker-build docker-run

# Build the application
build:
	go build -o bin/shop-api main.go

# Run the application locally
run:
	go run main.go

# Run tests
test:
	go test ./tests/... -v

# Clean build artifacts
clean:
	rm -rf bin/

# Build Docker image
docker-build:
	docker build -t shop-api .

# Run with Docker Compose
docker-run:
	docker-compose up --build

# Stop Docker Compose
docker-stop:
	docker-compose down

# Run tests in Docker
docker-test:
	docker-compose exec app go test ./tests/... -v

# Initialize Go module
init:
	go mod init shop-api
	go mod tidy

# Format code
fmt:
	go fmt ./...

# Lint code
lint:
	golangci-lint run

# Development setup
dev-setup: init
	go mod download
	@echo "Development environment ready!"
.PHONY: build test test-race lint fmt clean run docker-build docker-up docker-down docker-deploy help

# Build the application
build:
	@echo "Building momento..."
	@go build -o bin/momento cmd/momento/main.go
	@echo "Build complete: bin/momento"

# Run tests
test:
	@echo "Running tests..."
	@go test ./... -coverprofile=coverage.out
	@go tool cover -html=coverage.out -o coverage.html
	@echo "Tests complete. Coverage report: coverage.html"

# Run tests with race detector
test-race:
	@echo "Running tests with race detector..."
	@go test ./... -race

# Run linter
lint:
	@echo "Running linter..."
	@golangci-lint run ./...

# Format code
fmt:
	@echo "Formatting code..."
	@go fmt ./...

# Clean build artifacts
clean:
	@echo "Cleaning..."
	@rm -rf bin/
	@rm -f coverage.out coverage.html
	@echo "Clean complete"

# Run the bot
run:
	@echo "Running momento..."
	@go run cmd/momento/main.go

# Build Docker image
docker-build:
	@echo "Building Docker image..."
	@docker build -f deployments/docker/Dockerfile -t momento-bot:latest .
	@echo "Docker build complete"

# Start development environment
docker-up:
	@echo "Starting development environment..."
	@docker-compose -f deployments/docker/docker-compose.yml up -d

# Stop development environment
docker-down:
	@echo "Stopping development environment..."
	@docker-compose -f deployments/docker/docker-compose.yml down

# Deploy to swarm
docker-deploy:
	@echo "Deploying to Docker Swarm..."
	@docker stack deploy -c deployments/docker/docker-stack.yml momento

# Run database migrations
migrate-up:
	@echo "Running migrations..."
	@go run cmd/migrate/main.go up

# Rollback migrations
migrate-down:
	@echo "Rolling back migrations..."
	@go run cmd/migrate/main.go down

# Help
help:
	@echo "Available targets:"
	@echo "  build         - Build the application"
	@echo "  test          - Run tests with coverage"
	@echo "  test-race     - Run tests with race detector"
	@echo "  lint          - Run golangci-lint"
	@echo "  fmt           - Format code"
	@echo "  clean         - Clean build artifacts"
	@echo "  run           - Run the bot"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-up     - Start development environment"
	@echo "  docker-down   - Stop development environment"
	@echo "  docker-deploy - Deploy to Docker Swarm"
	@echo "  migrate-up    - Run database migrations"
	@echo "  migrate-down  - Rollback database migrations"
	@echo "  help          - Show this help message"

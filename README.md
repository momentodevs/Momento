# Momento

Momento is an open source, fully functional Discord bot that includes moderation, reaction roles, music features, and so much more. 100% CUSTOMIZABLE AND SECURE.

## 🚀 Important: Go Rewrite in Progress!

The original Python Momento bot has been completely rewritten in **Go** for better performance, easier deployment, and modern architecture.

**👉 For the latest version, please visit:** [momento-go/](./momento-go/)

## Quick Start (Go Version)

```bash
cd momento-go

# Install dependencies
go mod download

# Copy configuration files
cp configs/config.yaml.example configs/config.yaml
cp configs/application.yml.example configs/application.yml
cp .env.example .env

# Edit configuration
nano configs/config.yaml
nano .env

# Build and run
make build
make run

# Or use Docker
make docker-up
```

## Features

- ✅ **Moderation**: Mute/unmute, message clearing, auto-moderation
- ✅ **Reaction Roles**: Assign roles via reactions or buttons
- ✅ **Music System**: Lavalink integration for high-quality audio playback
- ✅ **Welcome System**: Custom welcome messages and channels
- ✅ **Player Stats**: Track messages, songs, and more
- ✅ **Slash Commands**: Modern Discord application commands
- ✅ **Admin Tools**: Bot configuration and management
- ✅ **Logging System**: Comprehensive logging with configurable levels

## Technology Stack (Go Version)

| Component | Technology |
|-----------|-----------|
| Discord API | `discordgo` |
| Database ORM | `GORM` |
| Databases | PostgreSQL, MySQL, SQLite (default) |
| Music | Lavalink (via disgolink) |
| Config | Viper + YAML |
| Logging | Zap |
| Testing | testify + discordgo-mock |
| Deployment | Docker + Docker Compose |

## Installation

### Prerequisites

- Go 1.25 or higher
- PostgreSQL, MySQL, or SQLite (optional, defaults to SQLite)
- Docker (optional, for Lavalink)

### Quick Start

```bash
git clone https://github.com/momentodevs/momento.git
cd momento
cd momento-go

# Copy configuration files
cp configs/config.yaml.example configs/config.yaml
cp configs/application.yml.example configs/application.yml
cp .env.example .env

# Edit configuration with your values
nano configs/config.yaml
nano .env
```

## Docker Deployment

### Development

```bash
cd momento-go

# Make sure .env has your actual values:
nano .env

# Start all services (bot, PostgreSQL, Lavalink):
make docker-up

# To view logs:
make docker-logs

# To stop services:
make docker-down

# To clean up:
make docker-clean
```

### Production (Docker Swarm)

```bash
cd momento-go

# Create Docker secrets:
echo "your_bot_token" | docker secret create discord_token -
echo "your_db_password" | docker secret create db_password -
echo "your_lavalink_password" | docker secret create lavalink_password -

# Deploy stack:
make docker-deploy
```

## Configuration

### Environment Variables (`.env`)

```bash
# Required
DISCORD_TOKEN=your_bot_token

# Optional - Database (defaults to SQLite if not set)
DATABASE_TYPE=postgres
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=momento
DATABASE_USER=postgres
DATABASE_PASSWORD=your_database_password

# Optional - Lavalink
LAVALINK_PASSWORD=youshallnotpass
LAVALINK_HOST=localhost
LAVALINK_PORT=2333
```

See [momento-go/configs/config.yaml.example](momento-go/configs/config.yaml.example) for full configuration options.

## Development

### Running Tests

```bash
cd momento-go
make test          # Run tests with coverage
make test-race    # Run with race detector
```

### Code Quality

```bash
cd momento-go
make lint  # Run golangci-lint
make fmt   # Format code
```

### Building

```bash
cd momento-go
make build  # Build binary
```

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make build` | Build application |
| `make test` | Run tests with coverage |
| `make test-race` | Run tests with race detector |
| `make lint` | Run golangci-lint |
| `make fmt` | Format code |
| `make clean` | Clean build artifacts |
| `make run` | Run the bot |
| `make docker-build` | Build Docker image |
| `make docker-up` | Start development environment |
| `make docker-down` | Stop development environment |
| `make docker-logs` | View Docker logs |
| `make docker-clean` | Clean up Docker volumes and containers |
| `make docker-deploy` | Deploy to Docker Swarm |
| `make help` | Show all available commands |

## Roadmap

- [x] Phase 1: Foundation & Infrastructure
- [x] Phase 2: Command System (basic commands)
- [ ] Phase 3: Complete Command System (all commands)
- [ ] Phase 4: Moderation System
- [ ] Phase 5: Welcome System
- [ ] Phase 6: Player Stats
- [ ] Phase 7: Reaction & Button Roles
- [ ] Phase 8: Music System (Lavalink)
- [ ] Phase 9: Logging System
- [ ] Phase 10: Full Test Suite
- [ ] Phase 11: Documentation Completion

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

[MIT License](LICENSE)

## Credits

Original Python bot by momentodevs
Go rewrite by momentodevs

## Support

Join our [Discord server](https://discord.gg/Z69rsfKrut) for support!

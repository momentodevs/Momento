# Momento Go

Momento is an open source, fully functional Discord bot that includes moderation, reaction roles, music features, and so much more. 100% CUSTOMIZABLE AND SECURE. This is a complete rewrite of the original Python bot in Go.

## Features

- ✅ **Moderation**: Mute/unmute, message clearing, auto-moderation
- ✅ **Reaction Roles**: Assign roles via reactions or buttons
- ✅ **Music System**: Lavalink integration for high-quality audio playback
- ✅ **Welcome System**: Custom welcome messages and channels
- ✅ **Player Stats**: Track messages, songs, and more
- ✅ **Slash Commands**: Modern Discord application commands
- ✅ **Admin Tools**: Bot configuration and management
- ✅ **Logging System**: Comprehensive logging with configurable levels

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Discord API | `discordgo` |
| Database ORM | `GORM` |
| Databases | PostgreSQL, MySQL, SQLite (default) |
| Music | Lavalink (via disgolink) |
| Config | Viper + YAML |
| Logging | Zap |
| Testing | testify + discordgo-mock |

## Installation

### Prerequisites

- Go 1.21 or higher
- PostgreSQL, MySQL, or SQLite (optional, defaults to SQLite)
- Docker (optional, for Lavalink)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/momentodevs/momento-go.git
cd momento-go
```

2. Copy configuration files:
```bash
cp configs/config.yaml.example configs/config.yaml
cp configs/application.yml.example configs/application.yml
cp .env.example .env
```

3. Edit configuration:
```bash
# Edit bot configuration
nano configs/config.yaml

# Set environment variables (IMPORTANT!)
nano .env
```

Required environment variables in `.env`:
- `DISCORD_TOKEN` - Your bot token from https://discord.com/developers/applications

Optional for PostgreSQL/MySQL:
- `DB_PASSWORD` - Database password (only needed if DATABASE_TYPE=postgres or mysql)
- `LAVALINK_PASSWORD` - Lavalink server password (must match configs/application.yml)

For SQLite (default): No additional variables needed!

4. Build and run:
```bash
make build
make run
```

## Docker Deployment

### Development (Docker Compose)

```bash
cd momento-go

# 1. Create .env file from example
cp .env.example .env

# 2. Edit .env with your values
nano .env

# 3. Start all services (bot, PostgreSQL, Lavalink)
make docker-up

# To view logs
make docker-logs

# To stop services
make docker-down

# To clean up (remove volumes)
make docker-clean
```

**What gets started:**
- **momento-bot** - The Discord bot
- **momento-db** - PostgreSQL database (uses SQLite if DATABASE_TYPE not set)
- **momento-lavalink** - Audio/music server

**Configuration files are mounted as volumes:**
- `./configs/` → `/configs` in container
- `./logs/` → `/logs` in container
- You can edit configs without rebuilding the container!

---

### Production (Docker Swarm)

```bash
cd momento-go

# 1. Create Docker secrets
echo "your_bot_token" | docker secret create discord_token -
echo "your_db_password" | docker secret create db_password -
echo "your_lavalink_password" | docker secret create lavalink_password -

# 2. Deploy stack
make docker-deploy
```

**Production stack includes:**
- Resource limits and restart policies
- Health checks
- Secret-based password management
- Proper volume management
- Service discovery via overlay network

---

## Configuration

### Bot Configuration (`configs/config.yaml`)

```yaml
discord:
  token: ""  # Use DISCORD_TOKEN env var (recommended)
  owner_id: ""  # Your Discord user ID
  coowners: []  # List of co-owner Discord IDs
  command_prefix: ["m?"]
  intents:
    - guilds
    - guild_messages
    - guild_members
    - message_content
    - voice_states

database:
  type: "sqlite"  # Options: sqlite, postgres, mysql
  host: "localhost"  # Required for postgres/mysql
  port: 5432  # Default: 5432 for postgres, 3306 for mysql
  database: "momento"
  user: "postgres"  # Default: postgres for postgres, mysql for mysql
  password: ""  # Use DB_PASSWORD env var (recommended)
  sslmode: "disable"  # Only for postgres

lavalink:
  host: "localhost"
  port: 2333
  password: "youshallnotpass"  # Use LAVALINK_PASSWORD env var (recommended)

bot:
  description: "Momento, A Multipurpose, opensource discord bot hosted 24/7"
  traceback: false
  pm_help: false

logging:
  level: "info"  # Options: debug, info, warn, error
  file: "discord.log"
  max_size: 100  # MB
  max_age: 30  # days
  max_backups: 3
```

### Lavalink Configuration (`configs/application.yml`)

```yaml
server:
  port: 2333
  address: 0.0.0.0

lavalink:
  server:
    password: "youshallnotpass"
    sources:
      youtube: true
      bandcamp: true
      soundcloud: true
      twitch: true
      vimeo: true
      http: true
      local: false

metrics:
  prometheus:
    enabled: false
    endpoint: /metrics

logging:
  file:
    max-history: 30
    max-size: 1GB
  level:
    root: INFO
    lavalink: INFO
```

---

## Commands

### Bot Commands

| Command | Description | Usage |
|---------|-------------|---------|
| `/ping` | Check bot latency | `/ping` |
| `/about` | Bot information | `/about` |
| `/serverinfo` | Server details | `/serverinfo` |
| `/stats [user]` | User statistics | `/stats @user` |

### Admin Commands

| Command | Description | Usage |
|---------|-------------|---------|
| `/prefix <prefix>` | Set command prefix | `/prefix !` |
| `/coowner add <user>` | Add co-owner | `/coowner add @user` |
| `/reload <extension>` | Reload extension | `/reload info` |
| `/shutdown` | Shutdown bot | `/shutdown` |

### Moderation Commands

| Command | Description | Usage |
|---------|-------------|---------|
| `/clear <amount>` | Delete messages | `/clear 10` |
| `/mute <user> [reason]` | Mute user | `/mute @user spam` |
| `/unmute <user>` | Unmute user | `/unmute @user` |

### Music Commands

| Command | Description | Usage |
|---------|-------------|---------|
| `/play <query>` | Play song/playlist | `/play https://youtube.com/watch?v=dQw4w9WgXcQ` |
| `/pause` | Pause playback | `/pause` |
| `/resume` | Resume playback | `/resume` |
| `/skip` | Skip current track | `/skip` |
| `/queue` | Show queue | `/queue` |
| `/volume <0-100>` | Set volume | `/volume 75` |
| `/leave` | Leave voice channel | `/leave` |

### Role Commands

| Command | Description | Usage |
|---------|-------------|---------|
| `/reaction_role create <emoji> <role>` | Create reaction role | `/reaction_role create 😎 @VIP` |
| `/button_role create <label> <role>` | Create button role | `/button_role create VIP @VIP` |

## Development

### Running Tests

```bash
make test          # Run tests with coverage
make test-race    # Run with race detector
```

### Code Quality

```bash
make lint  # Run golangci-lint
make fmt   # Format code
```

### Building

```bash
make build  # Build binary
```

### Docker Commands

```bash
make docker-build  # Build Docker image
make docker-up     # Start development environment
make docker-down   # Stop development environment
make docker-logs  # View service logs
make docker-clean  # Clean up volumes and containers
make docker-deploy # Deploy to Docker Swarm
```

## Project Structure

```
momento-go/
├── cmd/momento/main.go          # Entry point
├── internal/
│   ├── bot/bot.go              # Core bot with discordgo
│   ├── config/config.go          # Viper configuration
│   ├── database/database.go        # GORM + multi-driver support
│   ├── logger/logger.go          # Zap structured logging
│   ├── models/guild.go           # Database models
│   ├── commands/                 # Command handlers
│   ├── events/                    # Event listeners
│   ├── middleware/              # Permission checks, cooldowns
│   └── services/                 # Embed builders, Lavalink service
├── configs/
│   ├── config.yaml.example      # Bot configuration
│   └── application.yml.example # Lavalink configuration
├── Dockerfile                  # Multi-stage build (at root)
├── docker-compose.yml          # Development environment (at root)
├── docker-stack.yml           # Production Swarm (at root)
├── .env.example                # Environment variables template
├── Makefile                    # Common commands
├── go.mod/go.sum             # Dependencies
└── README.md                   # This file
```

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

---

## Quick Reference

### For Development

```bash
# Local development
make build && make run

# Docker development
make docker-up
```

### For Production

```bash
# Docker Swarm deployment
make docker-deploy
```

### Troubleshooting

**Bot not responding to commands:**
- Check DISCORD_TOKEN is set correctly
- Verify bot has proper intents in Discord developer portal
- Check logs: `make docker-logs`

**Database connection errors:**
- Verify DATABASE_TYPE matches your setup
- For PostgreSQL/MySQL: Check host, port, user, password
- Check if database is running: `docker compose ps`

**Lavalink not playing audio:**
- Verify LAVALINK_PASSWORD matches configs/application.yml
- Check Lavalink logs: `make docker-logs lavalink`
- Ensure bot has voice connection permissions

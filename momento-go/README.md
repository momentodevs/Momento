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
| Databases | PostgreSQL, MySQL, SQLite |
| Music | Lavalink (via disgolink) |
| Config | Viper + YAML |
| Logging | Zap |
| Testing | testify + discordgo-mock |

## Installation

### Prerequisites

- Go 1.21 or higher
- PostgreSQL, MySQL, or SQLite
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
cp .env.example .env
```

3. Edit configuration:
```bash
nano configs/config.yaml  # Update bot token, database, and other settings
nano .env  # Add sensitive data
```

4. Run migrations:
```bash
make migrate-up
```

5. Build and run:
```bash
make build
./bin/momento -config configs/config.yaml
```

## Docker Deployment

### Development

```bash
cp configs/config.yaml.example configs/config.yaml
cp .env.example .env
# Edit config files with your settings
make docker-up
```

### Production (Docker Swarm)

```bash
# First, create Docker secrets:
echo "your_bot_token" | docker secret create discord_token -
echo "your_db_password" | docker secret create db_password -
echo "your_lavalink_password" | docker secret create lavalink_password -

# Deploy stack:
make docker-deploy
```

## Configuration

### Basic Config (`configs/config.yaml`)

```yaml
discord:
  token: ""  # Use DISCORD_TOKEN env var
  owner_id: ""
  coowners: []
  command_prefix: ["m?"]
  intents:
    - guilds
    - guild_messages
    - guild_members
    - message_content
    - voice_states

database:
  type: "postgres"  # Options: postgres, mysql, sqlite
  host: "localhost"
  port: 5432
  database: "momento"
  user: "postgres"
  password: ""  # Use DB_PASSWORD env var

lavalink:
  host: "localhost"
  port: 2333
  password: "youshallnotpass"
```

### Environment Variables (`.env`)

```bash
DISCORD_TOKEN=your_bot_token
DB_PASSWORD=your_database_password
LAVALINK_PASSWORD=youshallnotpass
```

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

## Roadmap

- [x] Foundation & Infrastructure
- [x] Configuration System
- [x] Logging System
- [x] Database Layer (GORM)
- [x] Basic Commands (ping, about)
- [ ] Complete Command System
- [ ] Moderation System
- [ ] Welcome System
- [ ] Player Stats
- [ ] Reaction & Button Roles
- [ ] Music System (Lavalink)
- [ ] Logging System
- [ ] Full Test Suite
- [ ] Documentation

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

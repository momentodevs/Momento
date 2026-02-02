# AGENTS.md - Momento Bot Development Guide

This file provides guidelines for agentic coding assistants working on the Momento Discord music bot repository.

## Build Commands

### Go Backend
- Build: `go build -o Momento`
- Test all packages: `go test -v ./...`
- Test single package: `go test -v ./path/to/package`
- Test single function: `go test -v ./path/to/package -run TestFunctionName`
- Format code: `gofmt -w .`
- Tidy dependencies: `go mod tidy`

### Web Frontend (in `web/` directory)
- Development server: `pnpm run dev`
- Build for production: `pnpm run build`
- Lint: `pnpm run lint`
- Format: `pnpm run format`
- Preview build: `pnpm run preview`

### Docker
- Build: `docker build -t momento .`
- Compose: `docker-compose up`

## Code Style Guidelines

### Imports
- Group imports into three sections: standard library, third-party packages, internal packages
- Separate groups with blank lines
- Keep imports sorted alphabetically within each group

Example:
```go
import (
    "fmt"
    "os"

    "github.com/bwmarrin/discordgo"
    "github.com/gin-gonic/gin"

    "github.com/momentodevs/Momento/manager"
    "github.com/momentodevs/Momento/queue"
)
```

### Formatting
- Use `gofmt` for Go files (format before committing)
- Use `prettier` for web files (auto-applied via `pnpm run format`)
- Line length: reasonable, but favor readability over strict limits

### Types and Structures
- Exported types must have comments describing their purpose
- Use struct tags for JSON/config parsing (`json:"name"`, `fig:"configname"`)
- Define constants with `const` block when related
- Use atomic types (atomic.Bool, atomic.Uint64) for thread-safe counters

Example:
```go
type Server struct {
    Queue      queue.Queue  // The music queue
    Started    atomic.Bool   // Whether the job scheduler has started
    GuildID    string        // Discord guild ID
    Clients    *Clients      // API clients
}
```

### Naming Conventions
- Exported functions/types: PascalCase (e.g., `NewServer`, `GetVideo`)
- Private functions/types: camelCase (e.g., `downloadAndPlay`, `cleanURL`)
- Constants: PascalCase (e.g., `YoutubeBase`, `FrameSeconds`)
- Interfaces: Often end with "er" (e.g., `Reader`, `Writer`)
- Variables: camelCase, except for acronyms which remain uppercase (e.g., `VC`, `ID`)

### Error Handling
- Always check for errors: `if err != nil { ... }`
- Log errors using `lit.Error("Message: %s", err)`
- Return errors for expected failure conditions
- Use descriptive error messages

Example:
```go
response, err := y.client.Videos.List([]string{"snippet"}).Id(id).Do()
if err != nil {
    lit.Error("youtube GetVideo: %s", err.Error())
    return nil
}
```

### Concurrency
- Use `go func() { ... }()` for concurrent operations
- Use channels for communication between goroutines
- Use `defer` for cleanup (e.g., `defer mutex.Unlock()`)
- Use `sync.WaitGroup` to wait for goroutines
- Use atomic types for simple thread-safe operations

Example:
```go
serverMutex.Lock()
defer serverMutex.Unlock()

if _, ok := server[guild]; !ok {
    server[guild] = manager.NewServer(guild, &clients)
}
```

### Testing
- Test functions: `func TestFunctionName(t *testing.T) { ... }`
- Use table-driven tests for multiple test cases
- Use `t.Errorf()` for test failures with descriptive messages
- Place test files alongside source files (`*_test.go`)

Example:
```go
func TestIsValidUrl(t *testing.T) {
    if !IsValidURL("https://www.youtube.com/watch?v=dQw4w9WgXcQ") {
        t.Error("String is supposed to be a valid URL.")
    }
}
```

### Web/Svelte Conventions
- Use Svelte stores for state management (`writable`, `readable`)
- Import components from flowbite-svelte
- Use `onMount` lifecycle hook for initialization
- CamelCase for JavaScript variables and functions

### Database
- Use `database.ExecQuery()` for simple schema creation queries
- Use prepared statements for parameterized queries
- Handle `sql.ErrNoRows` as expected, not error
- Close connections properly with `defer db.Close()`

### Config Management
- Config file: `config.yml` (use `example_config.yml` as template)
- Use `fig` package for config parsing with struct tags
- Required fields: use `validate:"required"` tag
- Never commit `config.yml` with real tokens

## Project Structure

- `commands.go` - Discord slash command definitions and handlers
- `main.go` - Application entry point and initialization
- `manager/` - Core bot logic (play, pause, skip, queue management)
- `database/` - Database abstraction (MySQL/SQLite) and operations
- `api/` - REST API and WebSocket server
- `youtube/` - YouTube API integration
- `spotify/` - Spotify API integration
- `sponsorblock/` - SponsorBlock integration for ad skipping
- `web/` - SvelteKit frontend application
- `queue/` - Queue data structure and operations
- `vc/` - Discord voice connection management

## Important Notes

- The bot uses CGO for SQLite support
- External dependencies: `ffmpeg`, `yt-dlp`, `dca` must be installed
- Audio files cached in `audio_cache/` directory
- Database stored in `data/` directory
- Web build embedded in Go binary using embed directive
- Uses Discord slash commands exclusively (not prefix commands)

## Pre-commit Checklist

- [ ] Run `gofmt -w .` on Go files
- [ ] Run `go test ./...` to ensure tests pass
- [ ] Run `cd web && pnpm run lint` for frontend
- [ ] Verify `go build -o Momento` succeeds
- [ ] Check for TODO/FIXME comments and resolve if critical

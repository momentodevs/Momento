package bot

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/bwmarrin/discordgo"

	"github.com/momentodevs/momento-go/internal/config"
	"github.com/momentodevs/momento-go/internal/database"
	"github.com/momentodevs/momento-go/internal/logger"
)

type Bot struct {
	Session    *discordgo.Session
	Config     *config.Config
	DB         *database.Database
	StartTime  string
	Context    context.Context
	CancelFunc context.CancelFunc
}

func New(cfg *config.Config, db *database.Database) (*Bot, error) {
	session, err := discordgo.New(cfg.Discord.Token)
	if err != nil {
		return nil, fmt.Errorf("failed to create discord session: %w", err)
	}

	session.Identify.Intents = parseIntents(cfg.Discord.Intents)

	ctx, cancel := context.WithCancel(context.Background())

	bot := &Bot{
		Session:    session,
		Config:     cfg,
		DB:         db,
		StartTime:  time.Now().Format("2006-01-02 15:04:05"),
		Context:    ctx,
		CancelFunc: cancel,
	}

	session.AddHandler(func(s *discordgo.Session, r *discordgo.Ready) {
		bot.onReady(s, r)
	})

	session.AddHandler(func(s *discordgo.Session, i *discordgo.InteractionCreate) {
		bot.handleInteraction(s, i)
	})

	return bot, nil
}

func (b *Bot) Run() error {
	logger.Info("Starting bot...",
		logger.String("owner", b.Config.Discord.OwnerID),
		logger.Int64("guild_count", 0),
	)

	if err := b.Session.Open(); err != nil {
		return fmt.Errorf("failed to open websocket connection: %w", err)
	}

	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc

	logger.Info("Shutting down bot...")
	b.CancelFunc()

	if err := b.Session.Close(); err != nil {
		logger.Error("Error closing discord session", logger.Err(err))
	}

	if err := b.DB.Close(); err != nil {
		logger.Error("Error closing database", logger.Err(err))
	}

	logger.Sync()
	return nil
}

func (b *Bot) onReady(s *discordgo.Session, r *discordgo.Ready) {
	logger.Info("Bot is ready",
		logger.String("username", r.User.Username),
		logger.String("discriminator", r.User.Discriminator),
		logger.String("user_id", r.User.ID),
		logger.Int64("guild_count", int64(len(r.Guilds))),
	)

	fmt.Printf("\nLogged in as: %s#%s\n", r.User.Username, r.User.Discriminator)
	fmt.Printf("User ID: %s\n", r.User.ID)
	fmt.Printf("Connected to %d guilds\n\n", len(r.Guilds))
}

func (b *Bot) handleInteraction(s *discordgo.Session, i *discordgo.InteractionCreate) {
	if i.Type != discordgo.InteractionApplicationCommand {
		return
	}

	data := i.ApplicationCommandData()
	logger.Debug("Received slash command",
		logger.String("command", data.Name),
		logger.String("user", i.Member.User.Username),
	)

	// Commands will be handled here
	// switch data.Name {
	// case "ping":
	// 	b.handlePingCommand(s, i)
	// }
}

func parseIntents(intents []string) discordgo.Intent {
	var result discordgo.Intent

	for _, intent := range intents {
		switch intent {
		case "guilds":
			result |= discordgo.IntentGuilds
		case "guild_messages":
			result |= discordgo.IntentGuildMessages
		case "guild_members":
			result |= discordgo.IntentGuildMembers
		case "message_content":
			result |= discordgo.IntentMessageContent
		case "voice_states":
			result |= discordgo.IntentGuildVoiceStates
		}
	}

	return result
}

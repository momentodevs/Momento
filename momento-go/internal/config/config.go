package config

import (
	"fmt"
	"strings"

	"github.com/spf13/viper"
)

type Config struct {
	Discord  DiscordConfig  `mapstructure:"discord"`
	Database DatabaseConfig `mapstructure:"database"`
	Bot      BotConfig      `mapstructure:"bot"`
	Lavalink LavalinkConfig `mapstructure:"lavalink"`
	Logging  LoggingConfig  `mapstructure:"logging"`
}

type DiscordConfig struct {
	Token         string   `mapstructure:"token"`
	OwnerID       string   `mapstructure:"owner_id"`
	Coowners      []string `mapstructure:"coowners"`
	CommandPrefix []string `mapstructure:"command_prefix"`
	Intents       []string `mapstructure:"intents"`
}

type DatabaseConfig struct {
	Type     string `mapstructure:"type"`
	Host     string `mapstructure:"host"`
	Port     int    `mapstructure:"port"`
	Database string `mapstructure:"database"`
	User     string `mapstructure:"user"`
	Password string `mapstructure:"password"`
	SSLMode  string `mapstructure:"sslmode"`
}

type BotConfig struct {
	Description string `mapstructure:"description"`
	Traceback   bool   `mapstructure:"traceback"`
	PMHelp      bool   `mapstructure:"pm_help"`
}

type LavalinkConfig struct {
	Host     string       `mapstructure:"host"`
	Port     int          `mapstructure:"port"`
	Password string       `mapstructure:"password"`
	Nodes    []NodeConfig `mapstructure:"nodes"`
}

type NodeConfig struct {
	Name     string `mapstructure:"name"`
	Host     string `mapstructure:"host"`
	Port     int    `mapstructure:"port"`
	Password string `mapstructure:"password"`
	Region   string `mapstructure:"region"`
}

type LoggingConfig struct {
	Level      string `mapstructure:"level"`
	File       string `mapstructure:"file"`
	MaxSize    int    `mapstructure:"max_size"`
	MaxAge     int    `mapstructure:"max_age"`
	MaxBackups int    `mapstructure:"max_backups"`
}

func Load(configPath string) (*Config, error) {
	v := viper.New()

	v.SetConfigFile(configPath)
	v.SetConfigType("yaml")

	v.SetEnvPrefix("MOMENTO")
	v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
	v.AutomaticEnv()

	if err := v.ReadInConfig(); err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var cfg Config
	if err := v.Unmarshal(&cfg); err != nil {
		return nil, fmt.Errorf("failed to unmarshal config: %w", err)
	}

	if err := validate(&cfg); err != nil {
		return nil, fmt.Errorf("config validation failed: %w", err)
	}

	return &cfg, nil
}

func (c *Config) Validate() error {
	if c.Discord.Token == "" {
		return fmt.Errorf("discord token is required")
	}

	if c.Database.Type == "" {
		return fmt.Errorf("database type is required")
	}

	if c.Database.Type != "sqlite" && c.Database.Host == "" {
		return fmt.Errorf("database host is required for %s", c.Database.Type)
	}

	if len(c.Discord.Intents) == 0 {
		c.Discord.Intents = []string{
			"guilds",
			"guild_messages",
			"guild_members",
			"message_content",
			"voice_states",
		}
	}

	if c.Lavalink.Host == "" {
		c.Lavalink.Host = "localhost"
	}

	if c.Lavalink.Port == 0 {
		c.Lavalink.Port = 2333
	}

	if c.Logging.Level == "" {
		c.Logging.Level = "info"
	}

	return nil
}

func validate(cfg *Config) error {
	if cfg.Discord.Token == "" {
		return fmt.Errorf("discord token is required")
	}

	if cfg.Database.Type == "" {
		return fmt.Errorf("database type is required")
	}

	if cfg.Database.Type != "sqlite" && cfg.Database.Host == "" {
		return fmt.Errorf("database host is required for %s", cfg.Database.Type)
	}

	if len(cfg.Discord.Intents) == 0 {
		cfg.Discord.Intents = []string{
			"guilds",
			"guild_messages",
			"guild_members",
			"message_content",
			"voice_states",
		}
	}

	if cfg.Lavalink.Host == "" {
		cfg.Lavalink.Host = "localhost"
	}

	if cfg.Lavalink.Port == 0 {
		cfg.Lavalink.Port = 2333
	}

	if cfg.Logging.Level == "" {
		cfg.Logging.Level = "info"
	}

	return nil
}

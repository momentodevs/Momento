package main

import (
	"testing"

	"github.com/momentodevs/momento-go/internal/config"
)

func TestConfigLoad(t *testing.T) {
	tests := []struct {
		name    string
		path    string
		wantErr bool
	}{
		{
			name:    "non-existent file",
			path:    "/non/existent/config.yaml",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := config.Load(tt.path)
			if (err != nil) != tt.wantErr {
				t.Errorf("Load() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func TestConfigValidation(t *testing.T) {
	tests := []struct {
		name    string
		cfg     *config.Config
		wantErr bool
	}{
		{
			name: "missing token",
			cfg: &config.Config{
				Discord: config.DiscordConfig{
					Token: "",
				},
			},
			wantErr: true,
		},
		{
			name: "valid config",
			cfg: &config.Config{
				Discord: config.DiscordConfig{
					Token:   "valid_token",
					Intents: []string{"guilds"},
				},
				Database: config.DatabaseConfig{
					Type: "sqlite",
				},
			},
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.cfg.Validate()
			if (err != nil) != tt.wantErr {
				t.Errorf("Validate() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

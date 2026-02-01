package models

import (
	"time"

	"github.com/lib/pq"
)

type Guild struct {
	ID          string         `gorm:"primaryKey;size:20"`
	Prefix      string         `gorm:"size:50"`
	Description string         `gorm:"size:500"`
	MutedRoleID string         `gorm:"size:20"`
	Coowners    pq.StringArray `gorm:"type:text[]"`
	CreatedAt   time.Time
	UpdatedAt   time.Time

	WelcomeSettings WelcomeSettings `gorm:"foreignKey:GuildID"`
	RoleSettings    []RoleSetting   `gorm:"foreignKey:GuildID"`
	Users           []User          `gorm:"foreignKey:GuildID"`
}

type WelcomeSettings struct {
	GuildID   string `gorm:"primaryKey;size:20"`
	Enabled   bool
	ChannelID string `gorm:"size:20"`
	Message   string `gorm:"type:text"`
	CreatedAt time.Time
	UpdatedAt time.Time
}

type RoleSetting struct {
	ID        uint   `gorm:"primaryKey"`
	GuildID   string `gorm:"size:20;index"`
	Type      string `gorm:"size:20;index"`
	MessageID string `gorm:"size:20;index"`
	Emoji     string `gorm:"size:100"`
	Label     string `gorm:"size:100"`
	RoleID    string `gorm:"size:20;index"`
	CreatedAt time.Time
	UpdatedAt time.Time
}

type User struct {
	UserID    string `gorm:"primaryKey;size:20"`
	GuildID   string `gorm:"primaryKey;size:20;index"`
	Messages  int    `gorm:"default:0"`
	Songs     int    `gorm:"default:0"`
	JoinedAt  time.Time
	CreatedAt time.Time
	UpdatedAt time.Time
}

type MusicQueue struct {
	GuildID   string `gorm:"primaryKey;size:20;index"`
	Position  int    `gorm:"primaryKey;auto_increment"`
	TrackID   string `gorm:"size:100;index"`
	TrackData string `gorm:"type:json"`
	Requester string `gorm:"size:20"`
	CreatedAt time.Time
}

type LoggingSettings struct {
	GuildID         string `gorm:"primaryKey;size:20"`
	LogMessages     bool   `gorm:"default:false"`
	LogMessageEdits bool   `gorm:"default:false"`
	LogCommands     bool   `gorm:"default:false"`
	LogErrors       bool   `gorm:"default:false"`
	LogLevel        string `gorm:"size:20;default:'info'"`
	CreatedAt       time.Time
	UpdatedAt       time.Time
}

func (g *Guild) TableName() string {
	return "guilds"
}

func (ws *WelcomeSettings) TableName() string {
	return "welcome_settings"
}

func (rs *RoleSetting) TableName() string {
	return "role_settings"
}

func (u *User) TableName() string {
	return "users"
}

func (mq *MusicQueue) TableName() string {
	return "music_queues"
}

func (ls *LoggingSettings) TableName() string {
	return "logging_settings"
}

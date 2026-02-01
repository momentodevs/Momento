package database

import (
	"fmt"
	"time"

	"gorm.io/driver/mysql"
	"gorm.io/driver/postgres"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"github.com/momentodevs/momento-go/internal/config"
	"github.com/momentodevs/momento-go/internal/models"
)

type Database struct {
	*gorm.DB
}

var (
	DB *Database
)

func New(cfg *config.DatabaseConfig) (*Database, error) {
	var dialector gorm.Dialector

	switch cfg.Type {
	case "postgres":
		dsn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
			cfg.Host, cfg.Port, cfg.User, cfg.Password, cfg.Database, cfg.SSLMode)
		dialector = postgres.Open(dsn)
	case "mysql":
		dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
			cfg.User, cfg.Password, cfg.Host, cfg.Port, cfg.Database)
		dialector = mysql.Open(dsn)
	case "sqlite":
		dsn := cfg.Database
		if dsn == "" {
			dsn = "momento.db"
		}
		dialector = sqlite.Open(dsn)
	default:
		return nil, fmt.Errorf("unsupported database type: %s", cfg.Type)
	}

	db, err := gorm.Open(dialector, &gorm.Config{
		SkipDefaultTransaction: false,
		NowFunc: func() time.Time {
			return time.Now().UTC()
		},
	})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

	sqlDB, err := db.DB()
	if err != nil {
		return nil, fmt.Errorf("failed to get database instance: %w", err)
	}

	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetMaxOpenConns(100)
	sqlDB.SetConnMaxLifetime(time.Hour)

	database := &Database{DB: db}
	DB = database

	return database, nil
}

func (db *Database) AutoMigrate() error {
	return db.DB.AutoMigrate(
		&models.Guild{},
		&models.WelcomeSettings{},
		&models.RoleSetting{},
		&models.User{},
		&models.MusicQueue{},
		&models.LoggingSettings{},
	)
}

func (db *Database) Close() error {
	if db.DB != nil {
		sqlDB, err := db.DB.DB()
		if err == nil {
			return sqlDB.Close()
		}
	}
	return nil
}

func (db *Database) Ping() error {
	sqlDB, err := db.DB.DB()
	if err != nil {
		return err
	}
	return sqlDB.Ping()
}

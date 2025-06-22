package config

import (
	"log"
	"os"

	"github.com/jinzhu/gorm"
	_ "github.com/mattn/go-sqlite3"
)

func InitDB() *gorm.DB {
	dbPath := getEnv("DB_PATH", "./shopdb.sqlite")

	db, err := gorm.Open("sqlite3", dbPath)
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	log.Println("Database connected successfully")
	return db
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
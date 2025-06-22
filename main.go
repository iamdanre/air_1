package main

import (
	"log"
	"shop-api/config"
	"shop-api/models"
	"shop-api/routes"

	"github.com/gin-gonic/gin"
)

func main() {
	// Initialize database
	db := config.InitDB()
	defer db.Close()

	// Auto migrate models
	models.AutoMigrate(db)

	// Initialize test data
	models.InitTestData(db)

	// Setup Gin router
	r := gin.Default()

	// Setup routes
	routes.SetupRoutes(r, db)

	// Start server
	log.Println("Server starting on :8080")
	r.Run(":8080")
}

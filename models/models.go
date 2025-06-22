package models

import (
	"github.com/jinzhu/gorm"
)

type Customer struct {
	ID      uint   `json:"id" gorm:"primary_key"`
	Name    string `json:"name" gorm:"not null"`
	Surname string `json:"surname" gorm:"not null"`
	Email   string `json:"email" gorm:"unique;not null"`
}

type ShopItemCategory struct {
	ID          uint   `json:"id" gorm:"primary_key"`
	Title       string `json:"title" gorm:"not null"`
	Description string `json:"description"`
}

type ShopItem struct {
	ID          uint               `json:"id" gorm:"primary_key"`
	Title       string             `json:"title" gorm:"not null"`
	Description string             `json:"description"`
	Price       float64            `json:"price" gorm:"not null"`
	Categories  []ShopItemCategory `json:"categories" gorm:"many2many:shop_item_categories;"`
}

type OrderItem struct {
	ID       uint     `json:"id" gorm:"primary_key"`
	ShopItem ShopItem `json:"shop_item" gorm:"foreignkey:ShopItemID"`
	ShopItemID uint   `json:"shop_item_id"`
	Quantity int      `json:"quantity" gorm:"not null"`
}

type Order struct {
	ID         uint        `json:"id" gorm:"primary_key"`
	Customer   Customer    `json:"customer" gorm:"foreignkey:CustomerID"`
	CustomerID uint        `json:"customer_id"`
	Items      []OrderItem `json:"items" gorm:"many2many:order_items;"`
}

func AutoMigrate(db *gorm.DB) {
	db.AutoMigrate(&Customer{})
	db.AutoMigrate(&ShopItemCategory{})
	db.AutoMigrate(&ShopItem{})
	db.AutoMigrate(&OrderItem{})
	db.AutoMigrate(&Order{})
}

func InitTestData(db *gorm.DB) {
	// Create test customers
	customers := []Customer{
		{Name: "John", Surname: "Doe", Email: "john.doe@example.com"},
		{Name: "Jane", Surname: "Smith", Email: "jane.smith@example.com"},
	}
	for _, customer := range customers {
		db.FirstOrCreate(&customer, Customer{Email: customer.Email})
	}

	// Create test categories
	categories := []ShopItemCategory{
		{Title: "Electronics", Description: "Electronic devices and gadgets."},
		{Title: "Books", Description: "Literature, fiction, and non-fiction books."},
	}
	for _, category := range categories {
		db.FirstOrCreate(&category, ShopItemCategory{Title: category.Title})
	}

	// Create test shop items
	var electronics, books ShopItemCategory
	db.Where("title = ?", "Electronics").First(&electronics)
	db.Where("title = ?", "Books").First(&books)

	shopItems := []ShopItem{
		{Title: "Smartphone", Description: "Latest smartphone with modern features.", Price: 699.99, Categories: []ShopItemCategory{electronics}},
		{Title: "Science Fiction Novel", Description: "A thrilling sci-fi adventure.", Price: 19.99, Categories: []ShopItemCategory{books}},
	}
	for _, item := range shopItems {
		db.FirstOrCreate(&item, ShopItem{Title: item.Title})
	}
}
package handlers

import (
	"net/http"
	"shop-api/models"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
)

type ShopItemHandler struct {
	DB *gorm.DB
}

func NewShopItemHandler(db *gorm.DB) *ShopItemHandler {
	return &ShopItemHandler{DB: db}
}

func (h *ShopItemHandler) GetShopItems(c *gin.Context) {
	var items []models.ShopItem
	h.DB.Preload("Categories").Find(&items)
	c.JSON(http.StatusOK, items)
}

func (h *ShopItemHandler) GetShopItem(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	var item models.ShopItem
	if err := h.DB.Preload("Categories").First(&item, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Shop item not found"})
		return
	}

	c.JSON(http.StatusOK, item)
}

func (h *ShopItemHandler) CreateShopItem(c *gin.Context) {
	var item models.ShopItem
	if err := c.ShouldBindJSON(&item); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.DB.Create(&item).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create shop item"})
		return
	}

	c.JSON(http.StatusCreated, item)
}

func (h *ShopItemHandler) UpdateShopItem(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	var item models.ShopItem
	if err := h.DB.First(&item, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Shop item not found"})
		return
	}

	if err := c.ShouldBindJSON(&item); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	h.DB.Save(&item)
	c.JSON(http.StatusOK, item)
}

func (h *ShopItemHandler) DeleteShopItem(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	if err := h.DB.Delete(&models.ShopItem{}, id).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete shop item"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Shop item deleted successfully"})
}

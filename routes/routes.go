package routes

import (
    "shop-api/handlers"

    "github.com/gin-gonic/gin"
    "github.com/jinzhu/gorm"
)

func SetupRoutes(r *gin.Engine, db *gorm.DB) {
    // Initialize handlers
    customerHandler := handlers.NewCustomerHandler(db)
    categoryHandler := handlers.NewCategoryHandler(db)
    shopItemHandler := handlers.NewShopItemHandler(db)
    orderHandler := handlers.NewOrderHandler(db)

    // API routes
    api := r.Group("/api/v1")
    {
        // Customer routes
        customers := api.Group("/customers")
        {
            customers.GET("", customerHandler.GetCustomers)
            customers.GET("/:id", customerHandler.GetCustomer)
            customers.POST("", customerHandler.CreateCustomer)
            customers.PUT("/:id", customerHandler.UpdateCustomer)
            customers.DELETE("/:id", customerHandler.DeleteCustomer)
        }

        // Category routes
        categories := api.Group("/categories")
        {
            categories.GET("", categoryHandler.GetCategories)
            categories.GET("/:id", categoryHandler.GetCategory)
            categories.POST("", categoryHandler.CreateCategory)
            categories.PUT("/:id", categoryHandler.UpdateCategory)
            categories.DELETE("/:id", categoryHandler.DeleteCategory)
        }

        // Shop item routes
        shopItems := api.Group("/shopitems")
        {
            shopItems.GET("", shopItemHandler.GetShopItems)
            shopItems.GET("/:id", shopItemHandler.GetShopItem)
            shopItems.POST("", shopItemHandler.CreateShopItem)
            shopItems.PUT("/:id", shopItemHandler.UpdateShopItem)
            shopItems.DELETE("/:id", shopItemHandler.DeleteShopItem)
        }

        // Order routes
        orders := api.Group("/orders")
        {
            orders.GET("", orderHandler.GetOrders)
            orders.GET("/:id", orderHandler.GetOrder)
            orders.POST("", orderHandler.CreateOrder)
            orders.PUT("/:id", orderHandler.UpdateOrder)
            orders.DELETE("/:id", orderHandler.DeleteOrder)
        }
    }
}

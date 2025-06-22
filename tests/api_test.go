package tests

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "net/http/httptest"
    "shop-api/models"
    "shop-api/routes"
    "testing"

    "github.com/gin-gonic/gin"
    "github.com/jinzhu/gorm"
    _ "github.com/mattn/go-sqlite3"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func setupTestDB(t *testing.T) (*gin.Engine, *gorm.DB) {
    // Use in-memory SQLite for testing
    db, err := gorm.Open("sqlite3", ":memory:")
    require.NoError(t, err, "Failed to connect to test database")

    // Ensure database closes after test
    t.Cleanup(func() {
        err := db.Close()
        if err != nil {
            t.Logf("Warning: Failed to close test database: %v", err)
        }
    })

    // Auto-migrate database schema
    err = db.AutoMigrate(&models.Customer{}, &models.ShopItemCategory{}, &models.ShopItem{}, &models.OrderItem{}, &models.Order{}).Error
    require.NoError(t, err, "Failed to migrate test database")

    gin.SetMode(gin.TestMode)
    r := gin.New()
    routes.SetupRoutes(r, db)

    return r, db
}

func TestCustomerCRUD(t *testing.T) {
    router, db := setupTestDB(t)

    // Test Create Customer
    customer := models.Customer{
        Name:    "Test",
        Surname: "User",
        Email:   "test@example.com",
    }

    jsonData, err := json.Marshal(customer)
    require.NoError(t, err, "Failed to marshal customer JSON")

    req, err := http.NewRequest("POST", "/api/v1/customers", bytes.NewBuffer(jsonData))
    require.NoError(t, err, "Failed to create POST request")
    req.Header.Set("Content-Type", "application/json")

    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusCreated, w.Code)

    // Parse the created customer to get the ID
    var createdCustomer models.Customer
    err = json.Unmarshal(w.Body.Bytes(), &createdCustomer)
    require.NoError(t, err, "Failed to parse created customer response")
    require.NotZero(t, createdCustomer.ID, "Created customer should have a valid ID")

    customerID := createdCustomer.ID

    // Verify customer was actually saved to database
    var dbCustomer models.Customer
    err = db.First(&dbCustomer, customerID).Error
    require.NoError(t, err, "Customer should exist in database")
    assert.Equal(t, customer.Name, dbCustomer.Name)
    assert.Equal(t, customer.Surname, dbCustomer.Surname)
    assert.Equal(t, customer.Email, dbCustomer.Email)

    // Test Get Customers
    req, err = http.NewRequest("GET", "/api/v1/customers", nil)
    require.NoError(t, err, "Failed to create GET request")

    w = httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    var customerList []models.Customer
    err = json.Unmarshal(w.Body.Bytes(), &customerList)
    require.NoError(t, err, "Failed to parse customers list response")
    assert.Len(t, customerList, 1, "Should have exactly one customer")

    // Test Get Customer by ID
    req, err = http.NewRequest("GET", "/api/v1/customers/"+fmt.Sprintf("%d", customerID), nil)
    require.NoError(t, err, "Failed to create GET by ID request")

    w = httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    var retrievedCustomer models.Customer
    err = json.Unmarshal(w.Body.Bytes(), &retrievedCustomer)
    require.NoError(t, err, "Failed to parse retrieved customer response")
    assert.Equal(t, customerID, retrievedCustomer.ID)
    assert.Equal(t, customer.Name, retrievedCustomer.Name)

    // Test Update Customer
    updatedCustomer := models.Customer{
        Name:    "Updated",
        Surname: "User",
        Email:   "updated@example.com",
    }

    jsonData, err = json.Marshal(updatedCustomer)
    require.NoError(t, err, "Failed to marshal updated customer JSON")

    req, err = http.NewRequest("PUT", "/api/v1/customers/"+fmt.Sprintf("%d", customerID), bytes.NewBuffer(jsonData))
    require.NoError(t, err, "Failed to create PUT request")
    req.Header.Set("Content-Type", "application/json")

    w = httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    // Verify update in database
    err = db.First(&dbCustomer, customerID).Error
    require.NoError(t, err, "Updated customer should exist in database")
    assert.Equal(t, updatedCustomer.Name, dbCustomer.Name)
    assert.Equal(t, updatedCustomer.Email, dbCustomer.Email)

    // Test Delete Customer
    req, err = http.NewRequest("DELETE", "/api/v1/customers/"+fmt.Sprintf("%d", customerID), nil)
    require.NoError(t, err, "Failed to create DELETE request")

    w = httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    // Verify deletion in database
    err = db.First(&dbCustomer, customerID).Error
    assert.Error(t, err, "Customer should not exist in database after deletion")
    assert.True(t, gorm.IsRecordNotFoundError(err), "Should get record not found error")
}

func TestCategoryCRUD(t *testing.T) {
    router, db := setupTestDB(t)

    // Test Create Category
    category := models.ShopItemCategory{
        Title:       "Test Category",
        Description: "Test Description",
    }

    jsonData, err := json.Marshal(category)
    require.NoError(t, err, "Failed to marshal category JSON")

    req, err := http.NewRequest("POST", "/api/v1/categories", bytes.NewBuffer(jsonData))
    require.NoError(t, err, "Failed to create POST request")
    req.Header.Set("Content-Type", "application/json")

    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusCreated, w.Code)

    // Parse the created category to get the ID
    var createdCategory models.ShopItemCategory
    err = json.Unmarshal(w.Body.Bytes(), &createdCategory)
    require.NoError(t, err, "Failed to parse created category response")
    require.NotZero(t, createdCategory.ID, "Created category should have a valid ID")

    // Verify category was actually saved to database
    var dbCategory models.ShopItemCategory
    err = db.First(&dbCategory, createdCategory.ID).Error
    require.NoError(t, err, "Category should exist in database")
    assert.Equal(t, category.Title, dbCategory.Title)
    assert.Equal(t, category.Description, dbCategory.Description)

    // Test Get Categories
    req, err = http.NewRequest("GET", "/api/v1/categories", nil)
    require.NoError(t, err, "Failed to create GET request")

    w = httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    var categoryList []models.ShopItemCategory
    err = json.Unmarshal(w.Body.Bytes(), &categoryList)
    require.NoError(t, err, "Failed to parse categories list response")
    assert.Len(t, categoryList, 1, "Should have exactly one category")
    assert.Equal(t, category.Title, categoryList[0].Title)
}

func TestShopItemCRUD(t *testing.T) {
    router, db := setupTestDB(t)

    // Test Create Shop Item
    shopItem := models.ShopItem{
        Title:       "Test Item",
        Description: "Test Description",
        Price:       99.99,
    }

    jsonData, err := json.Marshal(shopItem)
    require.NoError(t, err, "Failed to marshal shop item JSON")

    req, err := http.NewRequest("POST", "/api/v1/shopitems", bytes.NewBuffer(jsonData))
    require.NoError(t, err, "Failed to create POST request")
    req.Header.Set("Content-Type", "application/json")

    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusCreated, w.Code)

    // Parse the created shop item to get the ID
    var createdShopItem models.ShopItem
    err = json.Unmarshal(w.Body.Bytes(), &createdShopItem)
    require.NoError(t, err, "Failed to parse created shop item response")
    require.NotZero(t, createdShopItem.ID, "Created shop item should have a valid ID")

    // Verify shop item was actually saved to database
    var dbShopItem models.ShopItem
    err = db.First(&dbShopItem, createdShopItem.ID).Error
    require.NoError(t, err, "Shop item should exist in database")
    assert.Equal(t, shopItem.Title, dbShopItem.Title)
    assert.Equal(t, shopItem.Description, dbShopItem.Description)
    assert.Equal(t, shopItem.Price, dbShopItem.Price)

    // Test Get Shop Items
    req, err = http.NewRequest("GET", "/api/v1/shopitems", nil)
    require.NoError(t, err, "Failed to create GET request")

    w = httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    var shopItemList []models.ShopItem
    err = json.Unmarshal(w.Body.Bytes(), &shopItemList)
    require.NoError(t, err, "Failed to parse shop items list response")
    assert.Len(t, shopItemList, 1, "Should have exactly one shop item")
    assert.Equal(t, shopItem.Title, shopItemList[0].Title)
}

func TestOrderCRUD(t *testing.T) {
    router, db := setupTestDB(t)

    // First create a customer to use for the order
    customer := models.Customer{
        Name:    "Order Customer",
        Surname: "Test",
        Email:   "order@example.com",
    }
    err := db.Create(&customer).Error
    require.NoError(t, err, "Failed to create test customer")
    require.NotZero(t, customer.ID, "Created customer should have a valid ID")

    // Test Create Order
    order := models.Order{
        CustomerID: customer.ID,
    }

    jsonData, err := json.Marshal(order)
    require.NoError(t, err, "Failed to marshal order JSON")

    req, err := http.NewRequest("POST", "/api/v1/orders", bytes.NewBuffer(jsonData))
    require.NoError(t, err, "Failed to create POST request")
    req.Header.Set("Content-Type", "application/json")

    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusCreated, w.Code)

    // Parse the created order to get the ID
    var createdOrder models.Order
    err = json.Unmarshal(w.Body.Bytes(), &createdOrder)
    require.NoError(t, err, "Failed to parse created order response")
    require.NotZero(t, createdOrder.ID, "Created order should have a valid ID")

    // Verify order was actually saved to database
    var dbOrder models.Order
    err = db.First(&dbOrder, createdOrder.ID).Error
    require.NoError(t, err, "Order should exist in database")
    assert.Equal(t, customer.ID, dbOrder.CustomerID)

    // Test Get Orders
    req, err = http.NewRequest("GET", "/api/v1/orders", nil)
    require.NoError(t, err, "Failed to create GET request")

    w = httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    var orderList []models.Order
    err = json.Unmarshal(w.Body.Bytes(), &orderList)
    require.NoError(t, err, "Failed to parse orders list response")
    assert.Len(t, orderList, 1, "Should have exactly one order")
    assert.Equal(t, customer.ID, orderList[0].CustomerID)
}

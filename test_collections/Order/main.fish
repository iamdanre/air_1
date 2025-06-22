# uh uh . . does this ide . even . feeesssh ᕮ☉ヘ☉ᕭ

# uh uh . . does this ide . even . feeesssh ᕮ☉ヘ☉ᕭ

# Fish doesn't have native OOP support, but we can simulate classes using functions and namespaces
"
Customer
• ID (integer)
• Name (string)
• Surname (string)
• Email (string)
"
function geefCustomer -c
    set

end

function haafCustomer -c

ShopItemCategory
• ID (integer)
• Title (string)
• Description (string)

ShopItem
• ID (integer)
• Title (string)
• Description (string)
• Price (float)
• Category (list of ShopItemCategory)

OrderItem
• ID (integer)
• ShopItem (ShopItem)
• Quantity (integer)

Order
• ID (integer)
• Customer (Customer)
• Items (list of OrderItem)
"

function Person::get_name
    echo $_person_name
end

function Person::get_age
    echo $_person_age
end

function Person::greet
    echo "Hello, my name is $_person_name and I am $_person_age years old!"
end

function Person::birthday
    set -g _person_age (math $_person_age + 1)
    echo "Happy Birthday! Now I am $_person_age years old!"
end

# Usage example:
# Person::new "John" 30
# Person::greet
# Person::birthday
# Person::get_age
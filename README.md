# vending-machine
Vending Machine API

Installation Steps:

1. git clone <repo>
  
2. cd <repo>
  
3. pip install virtualenv (if you don't already have virtualenv installed)
  
4. virtualenv venv to create your new environment (called 'venv' here)
  
5. source venv/bin/activate to enter the virtual environment
  
6. pip install -r requirements.txt
  
Running the server from IDE:

1. python manage.py runserver
  

Exposed Endpoints:
  
  1. vending_machine/api/register  -  To create a new user account
  request method - POST
  Request body 
    username
    password
    role -  ('B' for Buyer or 'S' for Seller)
  access - All
  
  2. vending_machine/api/users/token - To obtain a JWT access Token for the User
  request method - POST
  Request body - (this should be registered for this step to work)
    username
    password
  access - All registered Users
  
  3. vending_machine/api/users/token - To refresh a JWT access Token for the User
  request method - POST
  Request body - (this should be registered for this step to work)
    username
    password
  access - All registered Users
  
  4. vending_machine/api/users/me - To get the details of logged in user.
   request method - GET
   Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
   access - Authenticated User
  
  5. vending_machine/api/users/changepwd - To change the passowrd of the logged in user.
  request method - PUT
  Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
  Request body
  old_password
  new_password
  confirm_password
  access - Authenticated User
  
  6. vending_machine/api/users/delete - To delete the user account.
  request method - DELETE
  Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
  access - Authenticated User
  
  7. vending_machine/api/users/deposit - To deposit money in user account (in cents).
  request method - PUT
  Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
  Request body
  amount - (5,10,20,50,100) accepted
  access - Authenticated Buyers only
  
  8. vending_machine/api/users/reset - To reset the deposit of the user account.
  request method - PUT
  Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
  access - Authenticated Buyers only
  
  9. vending_machine/api/products/create - To create a new Product.
  request method - PUT
  Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
  Request Body
    productName
    cost (should be greater than 0, integer)
    amountAvailable (should be greater than zero, integer)
  
  access - Authenticated Sellers only
  
  10. vending_machine/api/products/show - To show all Products.
  request method - GET
  access - All
  
  11. vending_machine/api/products/delete - To delete a specific product.
  request method - DELETE
  Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
  Request Body
    productName
  access - Authenticated Sellers only
  
  12. vending_machine/api/products/update - To update/modify a specific product.
  request method - PUT
  Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
  Request Body
    productName
    cost (should be greater than 0, integer)
    amountAvailable (should be greater than zero, integer)
  access - Authenticated Sellers only
  
  13. vending_machine/api/products/buy - To buy a specific product.
  request method - PUT
  Authorization header (bearer token - <add the token got in point 2 or 3> in postman)
  Request Body
    productName
    sellerId
    quantity (should be greater than zero, integer)
  access - Authenticated Buyers only
  

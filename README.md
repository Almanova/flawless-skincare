# Flawless Skincare

Flawless Skincare is an API for e-commerce application. It includes such features as user management, browsing skincare products by categories, adding products to the cart, creating order and in-app purchases.

## Prerequisites

API uses PostgreSQL database, so in order to run the application locally, make sure that PostgreSQL is installed.

## Installation

1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the dependencies from the requirements.txt file

```bash
pip install requirements.txt
```

2. Create PostgreSQL database for the project

```bash
create database database_name owner user_name;
```

3. Add .env file to the project

4. Run the migrations, or use the dump for the database

```bash
./manage.py migrate
```

5. Run server

```bash
./manage.py runserver
```

## Apps

Project consists of 3 main applications: **auth**, **core** and **payment**.

**Auth** app is responsible for user management and contains endpoints for registration, login, creating and updating user profile and user information.

**Core** app is the main app responsible for all the logic of the skincare products online-store. Enables features of adding and browsing available products, adding products to the cart, adding products to the favourites, posting reviews and creating orders.

**Payment** is responsible for making online-transactions, storing transactions information.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Additional Links

[Detailed description of the functionality and features](https://docs.google.com/document/d/1kplucJaUD2Kl-eHKexpt4Y27vbGanuDsdoTVGp4k5Tg/edit?usp=sharing)

[Class Diagram](https://drive.google.com/file/d/1Xo3YzOBBZagE3fqCHbEYXfk6a7HEytrR/view?usp=sharing)
Flask + MongoDB API
This project is a REST API implemented using Flask, MongoDB and JWT authentication. The API supports product, user and order management.

Requirements

- Python 3.8+
- MongoDB
- VS Code (or other code editor)
- Postman (for API testing, optional)

Installation

1. **Clone the repository:**
   git clone <https://github.com/QaissAA/web_assignment3>
   cd <assign3>
   

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate # For Linux/macOS
   venv\Scripts\activate # For Windows
   

3. Install dependencies:

   pip install flask flask_pymongo flask_bcrypt flask_jwt_extended flask_cors python-dotenv pymongo


4. Create an .env file and add configuration:**
   In the root of the project, create an `.env` file and add to it:

   MONGO_URI=mongodb://localhost:27017/your_database
   JWT_SECRET_KEY=your_secret_key
   Replace `your_database` and `your_secret_key` with your data.

Start the Flask server
python assign3.py


The server will start at ``http://127.0.0.1:5000/``.
 Start the frontend (if any)
If the frontend is static files (e.g. HTML, CSS, JS), run it locally:


cd frontend

python -m http.server 5500


Then open `http://127.0.0.1:5500/` in a browser.

API Endpoints.

Authentication

`POST /api/users/register` - user registration
`POST /api/users/login` - user login

 Products

`POST /api/products` - add product
``PUT /api/products/<product_id>` - update product
`PUT /api/products/<product_id>` - update product
`DELETE /api/products/<product_id>` - delete product

Orders

-`POST /api/orders` - create order (JWT required)
-`GET /api/orders` - get user's orders (JWT required)
 `PUT /api/orders/<order_id>` - update order status (JWT required)

Errors and their solutions

CORS Policy Error:Make sure Flask is configured to work with CORS. You can add ``Flask-CORS``:

  pip install flask-cors

  And add to ``app.py``:

  from flask_cors import CORS
  CORS(app)

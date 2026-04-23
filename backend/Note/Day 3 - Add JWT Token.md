# 🧠 SYSTEM OVERVIEW
- This is a User Authentication System for a booking application. It handles user registration, login, and JWT token generation. The system verifies user credentials, hashes passwords for security, and issues access tokens for protected routes.

# 🔄 SYSTEM FLOW
Step 1: Client sends login request with email/password to `/token` endpoint  
Step 2: Router receives OAuth2 form data and calls `authenticate_user()`  
Step 3: Security utility queries database to find user by email  
Step 4: System verifies password hash matches stored hash  
Step 5: If valid, system creates JWT access token with expiration  
Step 6: Returns token to client for future authenticated requests  

# 📁 FILE: routers/users.py
## 🎯 Purpose
- Defines API endpoints for user registration and login. Acts as the HTTP interface for authentication.

## ⚙️ Main Components
- `register_user()` - Handles new user signup with email/password
- `login()` - Authenticates users and returns JWT token

## 🔍 CODE WALKTHROUGH
- **Line 16-32 (Register)**: Checks if email exists → raises 400 error if duplicate → calls `create_user()` to save → returns new user
- **Line 34-51 (Login)**: Uses `OAuth2PasswordRequestForm` for standard login format → calls `authenticate_user()` to verify credentials → raises 401 if invalid → creates access token with expiration time → returns `Token` object with bearer type
- **Line 39-40**: Uses `Depends()` for session injection - FastAPI handles database connection automatically
- **Line 42-46**: Returns proper HTTP 401 with "WWW-Authenticate" header for OAuth2 compliance

## 🔗 HOW IT CONNECTS
- **Called by**: Frontend apps, mobile apps, or API clients via HTTP POST
- **Calls**: `crud/users.py` (get_user_by_email, create_user), `security.py` (authenticate_user, create_access_token)

---

# 📁 FILE: security.py
## 🎯 Purpose
- Handles all security-related operations: password hashing, password verification, and JWT token creation/validation.

## ⚙️ Main Components
- `hash_password()` - Converts plain password to secure hash
- `verify_password()` - Checks if plain password matches hash
- `create_access_token()` - Generates JWT token with expiration
- `authenticate_user()` - Validates user credentials against database

## 🔍 CODE WALKTHROUGH
- **Line 1-9**: Imports crypto tools (bcrypt for passwords, JWT for tokens), loads environment variables for security keys
- **Line 11**: Sets up OAuth2 scheme pointing to `/token` endpoint - tells FastAPI where to send login requests
- **Line 13**: Creates bcrypt password context - industry-standard password hasher
- **Line 15-17**: Loads config from environment (30 min default token expiry, secret key from .env file)
- **Line 19-20**: `hash_password()` - uses bcrypt to create secure hash (one-way encryption)
- **Line 23-24**: `verify_password()` - compares plain text password with stored hash safely
- **Line 27-35**: `create_access_token()` - copies user data, adds expiration timestamp, encodes as JWT with secret key
- **Line 38-44**: `authenticate_user()` - queries database for user by email → returns False if not found → verifies password → returns user object if valid

## 🔗 HOW IT CONNECTS
- **Called by**: `routers/users.py` (login function), `routers/users.py` (register function indirectly via CRUD)
- **Calls**: `models/users.py` (UserInDB for database query), database via SQLModel Session

---

# 📁 FILE: models/users.py (Inferred from imports)
## 🎯 Purpose
- Defines the User database table structure using SQLModel.

## ⚙️ Main Components
- `UserInDB` - SQLModel class representing users table with id, email, password fields

## 🔍 CODE WALKTHROUGH
- Uses `SQLModel` with `table=True` to create actual database table
- `id` field is UUID primary key (auto-generated)
- `email` field is unique and indexed for fast lookups
- `password` field stores bcrypt hash (never plain text)

## 🔗 HOW IT CONNECTS
- **Called by**: `security.py` (authenticate_user queries this table), `alembic/env.py` (for migrations)
- **Calls**: PostgreSQL database

---

# 🔐 KEY SECURITY CONCEPTS

## Password Hashing (bcrypt)
- **Why**: Never store plain passwords. If database is hacked, attackers can't read passwords
- **How**: bcrypt adds random "salt" to each password before hashing
- **Result**: Same password produces different hash each time

## JWT Tokens
- **What**: JSON Web Token = encoded user data + signature
- **Payload**: Contains user email ("sub") + expiration time ("exp")
- **Signature**: Created with SECRET_KEY - proves token is authentic
- **Expiration**: Token becomes invalid after 30 minutes (configurable)

## OAuth2PasswordBearer
- **Standard**: Follows OAuth2 specification for login
- **Flow**: Client sends form data → server returns token → client uses "Bearer {token}" in headers
- **Header**: `Authorization: Bearer eyJhbGc...`

---

# 🚨 ERROR HANDLING

## Registration Errors
- **400 Bad Request**: Email already registered (prevents duplicates)

## Login Errors  
- **401 Unauthorized**: Wrong email or password
- **WWW-Authenticate Header**: Tells client this is OAuth2 protected

## Security Notes
- **SECRET_KEY**: Must be random and kept secret (in .env file)
- **ALGORITHM**: Uses HS256 (HMAC with SHA-256)
- **Expiration**: Tokens expire to limit damage if stolen
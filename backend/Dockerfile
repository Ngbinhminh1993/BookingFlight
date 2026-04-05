# 1. Choose a base image (Python environment)
FROM python:3.12-slim  
# -> "slim" = smaller, faster image (good for production)

# 2. Install uv tool (like pip but faster)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# -> Copy uv binary from another image into this container
# -> /bin = place where executable commands live
# -> After this, we can use "uv" inside container

# 3. Copy your project code into container
COPY . /app
# -> "." = everything in your current folder
# -> "/app" = folder inside container

# 4. Move into app directory
WORKDIR /app
# -> All next commands will run inside /app

# 5. Install dependencies
RUN uv sync --frozen --no-cache
# -> Install packages from lock file (like requirements.txt but better)
# -> --frozen = MUST match exact versions (safe & reproducible)
# -> --no-cache = don't store cache (smaller image)

CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]

# CMD = default command that runs when container starts
# -> Think: "what should this container DO when it starts?"

# ================================
# 1. "/app/.venv/bin/fastapi"
# ================================
# -> This is the executable (the program to run)

# Why full path?
# -> uv created a virtual environment at /app/.venv
# -> Inside it: /bin/fastapi (CLI tool)
# -> We use it to ensure correct Python + dependencies

# If you used just "fastapi" → may fail (PATH issues)
# So full path = safe + predictable

# Think:
# /app/.venv/bin/fastapi = "run FastAPI using my project's environment"


# ================================
# 2. "run"
# ================================
# -> This tells fastapi CLI: "start the server"

# Equivalent to:
# fastapi run main.py

# Behind the scenes:
# -> It runs a server (like uvicorn)
# -> Loads your FastAPI app


# ================================
# 3. "main.py"
# ================================
# -> Your application entry file

# It must contain something like:
# app = FastAPI()

# fastapi CLI will:
# -> open main.py
# -> find "app"
# -> run it

# IMPORTANT:
# If file name changes → must update here


# ================================
# 4. "--port", "80"
# ================================
# -> Run server on port 80 (inside container)

# Why 80?
# -> Default HTTP port (standard web)

# Docker mapping:
# docker run -p 8000:80
# -> 8000 (your machine) → 80 (container)

# So:
# browser → localhost:8000 → container:80


# ================================
# 5. "--host", "0.0.0.0"
# ================================
# -> This is CRITICAL in Docker

# What is 0.0.0.0?
# -> "listen on ALL network interfaces"

# Without this:
# default = 127.0.0.1 (localhost)

# Problem:
# 127.0.0.1 inside container ≠ your computer

# Result:
# ❌ Cannot access API from host

# With 0.0.0.0:
# ✅ Accept connections from outside container

# Think:
# 127.0.0.1 = private (only inside container)
# 0.0.0.0   = public (Docker can access)


# ================================
# WHY JSON ARRAY FORMAT?  (VERY IMPORTANT)
# ================================

# CMD ["program", "arg1", "arg2"]

# This is called "exec form"

# Advantages:
# ✅ No shell (faster, safer)
# ✅ No string parsing issues
# ✅ Signals handled correctly (important for production)

# BAD example:
# CMD fastapi run main.py --port 80 --host 0.0.0.0
# -> uses shell → less reliable


# ================================
# WHAT HAPPENS WHEN CONTAINER STARTS?
# ================================

# Step-by-step:
# 1. Container starts
# 2. Docker runs CMD
# 3. fastapi CLI starts server
# 4. Server listens on 0.0.0.0:80
# 5. You access via browser


# ================================
# SIMPLE MEMORY TRICK 🧠
# ================================

# CMD = Start app

# "/app/.venv/bin/fastapi"
# -> use correct Python environment

# "run main.py"
# -> start your app

# "--port 80"
# -> where app runs

# "--host 0.0.0.0"
# -> allow outside access (Docker magic)
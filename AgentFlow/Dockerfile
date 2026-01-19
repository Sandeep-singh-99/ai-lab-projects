# Stage 1: Build the client
FROM node:20-alpine AS client-builder

# Set Working directory for client
WORKDIR /app/client

# Copy client package files and install dependencies
COPY client/package.json ./
COPY client/package-lock.json ./

# If you use yarn and npm, adjust accordingly
RUN npm install

# Copy the rest of the client source code
COPY client/ ./

# Build the client
RUN npm run build

# Stage 2: Python backend
FROM docker.io/langchain/langgraph-api:3.11

# Install UV 
# First install curl, then install UV using the standlone installer
RUN apt-get update && apt-get install -y curl && \ 
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/api/lists/*
ENV PATH="/root/.local/bin:$PATH"

# -- End of UV installation --

# -- Copy built frontend from builder stage --
# The app.py expects the frontend build to be at ../frontend/dist relative to its own location.
# If app.py is at /deps/server/src/agent/app.py, then ../frontend/dist resolves to /deps/client/dist.
COPY --from=client-builder /app/client/dist /deps/client/dist
# -- End of copying built frontend --

# -- Adding local package . --
ADD server/ /deps/server
# -- End of local package . --

# -- Installing all local dependencies using UV --
# First, we need to ensure pip is available for UV to use
RUN uv pip install --system pip setuptools wheel
# Install dependencies with UV, respecting constraints
RUN cd /deps/server && \
    PYTHONDONTWRITEBYTECODE=1 UV_SYSTEM_PYTHON=1 uv pip install --system -c /api/constraints.txt -e .
# -- End of local dependencies install --
ENV LANGGRAPH_HTTP='{"app": "/deps/server/src/agent/app.py:app"}'
ENV LANGSERVE_GRAPHS='{"agent": "/deps/server/src/agent/graph.py:graph"}'

# -- Ensure user deps didn't inadvertently overwrite langgraph-api
# Create all required directories that the langgraph-api package expects
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license /api/langgraph_storage && \
    touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py /api/langgraph_storage/__init__.py
# Use pip for this specific package as it has poetry-based build requirements
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir --no-deps -e /api
# -- End of ensuring user deps didn't inadvertently overwrite langgraph-api --
# -- Removing pip from the final image (but keeping UV) --
RUN uv pip uninstall --system pip setuptools wheel && \
    rm -rf /usr/local/lib/python*/site-packages/pip* /usr/local/lib/python*/site-packages/setuptools* /usr/local/lib/python*/site-packages/wheel* && \
    find /usr/local/bin -name "pip*" -delete
# -- End of pip removal --

WORKDIR /deps/server


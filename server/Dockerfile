FROM python:3.10

ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container to the root of your Python project.
# This aligns with where your pyproject.toml and README.md are expected.
WORKDIR /jeffersonlab_phonebook/

# Install uv from ghcr.io
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

# Place executables in the environment at the front of the path
# This ensures that scripts installed by uv (like uvicorn) are found.
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/jeffersonlab_phonebook/.venv/bin:$PATH"

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# --- Build Stage: Install Dependencies ---
# Copy pyproject.toml, uv.lock, and README.md first for better Docker caching.
# These files are located in your 'server/' directory relative to the build context.
# They are copied to the current WORKDIR (/jeffersonlab_phonebook/) inside the container.
COPY pyproject.toml ./
COPY uv.lock ./
COPY README.md ./

# Install dependencies using uv sync --frozen --no-install-project.
# The bind mounts now correctly refer to files within the current WORKDIR.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./uv.lock,target=uv.lock \
    --mount=type=bind,source=./pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Set PYTHONPATH to include the application root for Python imports.
# This should match your WORKDIR.
ENV PYTHONPATH=/jeffersonlab_phonebook

# Copy the main Python package directory.
# This copies 'server/jeffersonlab_phonebook' from the build context
# to '/jeffersonlab_phonebook/jeffersonlab_phonebook' inside the container.
COPY jeffersonlab_phonebook ./jeffersonlab_phonebook


# Sync the project (install in editable mode)
# This uv sync will find pyproject.toml and README.md in /jeffersonlab_phonebook,
# allowing hatchling to build the editable wheel successfully.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Copy the entrypoint script and make it executable.
# It's located in 'server/entrypoint.sh' in your build context.
# It will be copied to '/jeffersonlab_phonebook/entrypoint.sh' inside the container.
#COPY entrypoint.sh ./
CMD ["uvicorn", "jeffersonlab_phonebook.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

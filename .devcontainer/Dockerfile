FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm@sha256:03eb80833c2482312891176cdfc1725c07513fc6a959c98b0a1cdb0db6d7354c
COPY --from=ghcr.io/astral-sh/uv:0.9.11@sha256:5aa820129de0a600924f166aec9cb51613b15b68f1dcd2a02f31a500d2ede568 /uv /uvx /bin/

# Install system dependencies for media processing and magic numbers.
RUN apt update
RUN apt install -y \
    libmagic1 \
    ffmpeg
RUN apt clean

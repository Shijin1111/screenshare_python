# Use a stable Ubuntu version
FROM ubuntu:22.04

# Set non-interactive mode to prevent timezone prompts
ENV DEBIAN_FRONTEND=noninteractive


# Update package lists and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip gcc g++ openjdk-17-jdk tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Default command
CMD ["/bin/bash"]


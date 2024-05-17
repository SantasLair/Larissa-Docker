# Use Ubuntu as the base image
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy the executable to the container
COPY geth-ubuntu-x86_64 /root/geth-ubuntu-x86_64
COPY config.toml /root/config.toml

# Make sure the executable is runnable
RUN chmod +x /root/geth-ubuntu-x86_64

# Set the environment variable
ENV LARISSA_NODE_USER_KEY=your_default_key
ENV CONFIG_TOML_FILE=config.toml

# Set working directory
WORKDIR /root

# Command to run the executable
CMD ./geth-ubuntu-x86_64 --larissa.node=1 --larissa.node.user.key=$LARISSA_NODE_USER_KEY --config=$CONFIG_TOML_FILE
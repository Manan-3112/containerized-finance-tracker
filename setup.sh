# For Ubuntu/Debian
sudo apt update && sudo apt install -y podman podman-compose

# OR for Fedora/RHEL (choose one based on your Linux distro)
# sudo dnf install -y podman podman-compose

# Verify installation
podman --version
podman-compose --version

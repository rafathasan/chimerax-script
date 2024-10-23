# Use a base image
FROM ubuntu:24.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install wget -y

# Download the UCSF ChimeraX .deb file
RUN wget -O /tmp/ucsf-chimerax.deb "https://www.rbvi.ucsf.edu/chimerax/cgi-bin/secure/chimerax-get.py?ident=OHeQer2WSqdn9uNyr3lc4f9xvkdWTNj%2F3hty1hTgifIpqe3I&file=1.8%2Fubuntu-24.04%2Fucsf-chimerax_1.8ubuntu24.04_amd64.deb&choice=Notified"

# Install necessary packages
RUN apt-get update && apt-get install -y \
    gdebi-core \
    ffmpeg \
    libegl1 \
    libfftw3-single3 \
    libgdk-pixbuf2.0-0 \
    libglu1-mesa

# Install the .deb package
RUN gdebi -n /tmp/ucsf-chimerax.deb

# Clean up
RUN rm /tmp/ucsf-chimerax.deb && rm -rf /var/lib/apt/lists/*

# Command to run when starting the container (modify as necessary)
ENTRYPOINT ["chimerax", "--nogui", "--exit"]

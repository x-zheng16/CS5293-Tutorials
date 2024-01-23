# Lists the files in your .ssh directory, if they exist
ll ~/.ssh

# Generate a new key if needed with RSA 2048⁄4096 or Ed25519
# Just don’t use ECDSA/DSA!
ssh-keygen -t ed25519

# Start the ssh-agent in the background
eval "$(ssh-agent -s)"

# Add your SSH private key to the ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to VM
ssh-copy-id seed@127.0.0.1 -p 8022

# Now try again to log in with no password required
ssh seed@127.0.0.1 -p 8022
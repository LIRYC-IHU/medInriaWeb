FROM kitware/trame:py3.9

# Copy the server directory
COPY --chown=trame-user:trame-user ./server /deploy/server

# Install Python dependencies
RUN cd /deploy/server && /deploy/server/venv/bin/pip install -e .

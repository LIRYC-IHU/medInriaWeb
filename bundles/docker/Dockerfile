FROM kitware/trame:py3.9

# Copy the server directory
COPY --chown=trame-user:trame-user ./server /deploy/server

# Install Python dependencies
RUN /deploy/server/venv/bin/pip install -r /deploy/server/requirements.txt

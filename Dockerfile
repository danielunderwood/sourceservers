FROM python:2

# Copy project files
WORKDIR /sourceservers
COPY . /sourceservers

# Expose port that uwsgi uses
EXPOSE 5555

# Install les and dependencies
RUN pip install .\[deploy\]

# Create user to run as and give permissions
RUN useradd sourceservers
RUN chown -R sourceservers:root /sourceservers

# Drop root privileges
USER sourceservers

# Start the UWSGI process. Entrypoint allows other uwsgi arguments to be
# supplied to the `docker run` command
ENTRYPOINT ["uwsgi", "--ini", "/sourceservers/deploy/uwsgi.ini"]

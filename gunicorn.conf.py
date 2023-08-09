# Gunicorn Settings.
timeout = 0  # Infinite timeouts for generating image processes.
workers = 2
bind = ["127.0.0.1:5000"]  # Can be changed to meet your needs.

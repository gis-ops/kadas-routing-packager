bind = "0.0.0.0:5000"
# Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off with
workers = 5
worker_class = 'gevent'
worker_connections = 10
timeout = 30
keepalive = 2

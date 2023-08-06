::


              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.5

    Build composable event pipeline servers with minimal effort.



    =========================
    wishbone.input.httpserver
    =========================

    Version: 1.0.2

    Receive events over HTTP.
    -------------------------


        An HTTP server mapping URL endpoints to queues to which events can be
        submitted.

        Mapping queues to endpoints:
        ---------------------------

        Connecting queues to this module automatically maps them to the equivalent
        URL enpoint.

        The "/" endpoint is by default mapped to the <outbox> queue.

        Available meta data:
        --------------------

        Each event has some meta associated stored in @tmp.<instance_name>:

            - remote_addr   : The client IP
            - request_method: The request method used
            - queue         : The name of the endpoint (and thus queue) to
                              which data was submitted.


        Parameters:

            - address(str)("0.0.0.0")
               |  The address to bind to.

            - port(int)(19283)
               |  The port to bind to.

            - keyfile(str)(None)
               |  When SSL is required, the location of the keyfile to use.

            - certfile(str)(None)
               |  When SSL is required, the location of the certfile to use.

            - ca_certs(str)(None)
                |  When SSL is required, the location of the ca certs to use.

            - delimiter(str)(None)
               |  The delimiter which separates multiple
               |  messages in a stream of data.

            - poolsize(int)(1000)
                |  The connection pool size.

            - so_reuseport(bool)(False)
                |  Enables socket option SO_REUSEPORT.
                |  See https://lwn.net/Articles/542629/
                |  Required when running multiple Wishbone instances.

            - response(str)("ok")*
                |  The value of the response.  Can be a lookup function.
                |  This value is also stored under @tmp.<module>.response


        Queues:

            - outbox
               |  Incoming events submitted to /

            - <queue_name>
               |  Incoming events submitted to /<queue_name>



import SocketServer
import json

import app.CreateNewOrganism.EssentialDataMain as EssentialDataMain

class ServerTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    '''
    id 1000 is fixed now. It will be change after define other job.
    '''
    function_dict = {}
    function_dict[1000] = 'EssentialDataMain.main'


    def handle(self):


        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        data = json.loads(self.data)

        function_name = self.function_dict[data['job_id']]
        eval(function_name)(data)



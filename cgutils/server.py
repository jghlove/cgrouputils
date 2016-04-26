import kvm_cgroup
import docker_cgroup
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            contentType = 'text/html'
            if self.path.startswith("/server/"):
                module = self.path.split('=')[1]
                output = subprocess.Popen(
                    serverPath + modulesSubPath + module + '.sh',
                    shell = True,
                    stdout = subprocess.PIPE)
                data = output.communicate()[0]
            self.send_response(200)
            self.send_header('Content-type', contentType)
            self.end_headers()
            self.wfile.write(data)
        except IOError:
            self.send_error(404, 'Filf Not Found')
if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 12345), MainHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
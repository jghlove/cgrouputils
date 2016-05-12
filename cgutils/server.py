import kvm_cgroup
import docker_cgroup
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import subprocess
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            contentType = 'text/html'
            modules = self.path.split('/')
            if len(modules) != 5:
                self.send_error(404, "api not found")
            if modules[1].equal('kvm'):
                if modules[2].equal('cpu'):
                    if modules[3].equal('set'):
                        vals = modules[4].split("&")
                        if len(vals) == 2:
                            cpu = kvm_cgroup.kvmCpuLimit(vals[0])
                            cpu.cpulimit(vals(1))
                    elif modules[3].equal('unset'):
                        uncpu = kvm_cgroup.kvmCpuLimit(modules[4])
                        uncpu.cpuunset()
                    else:
                        self.send_error(404, "api not found")
                elif modules[2].equal('cpuset'):
                    if modules[3].equal('set'):
                        vals = modules[4].split("&")
                        if len(vals) == 2:
                            cpuset = kvm_cgroup.kvmCpusetLimit(vals[0])
                            cpuset.cpusetlimit(vals(1))
                    elif modules[3].equal('unset'):
                        uncpuset = kvm_cgroup.kvmCpusetLimit(modules[4])
                        uncpuset.cpusetunset()
                    else:
                        self.send_error(404, "api not found")
                elif modules[2].equal('memory'):
                    if modules[3].equal('set'):
                        vals = modules[4].split("&")
                        if len(vals) == 2:
                            mem = kvm_cgroup.kvmMemLimit(vals[0])
                            mem.memlimit(vals(1))
                    elif modules[3].equal('unset'):
                        unmem = kvm_cgroup.kvmMemLimit(modules[4])
                        unmem.memunset()
                    else:
                        self.send_error(404, "api not found")
                elif modules[2].equal('blk_io'):
                    if modules[3].equal('set'):
                        vals = modules[4].split("&")
                        if 2 < len(vals) < 5:
                            disk = kvm_cgroup.kvmDiskLimit(vals[0])
                            if vals[1].equal('read'):
                                if len(vals)== 3:
                                    disk.diskreadlimit(vals[3])
                                else:
                                    disk.diskreadlimit(vals[3],vals[4])
                                disk.diskreadlimit(vals[3])
                            elif vals[1].equal('write'):
                                if len(vals) == 3:
                                    disk.diskwritelimit(vals[3])  
                                else:
                                    disk.diskwritelimit(vals[3], vals[4])
                    elif modules[3].equal('unset'):
                        vals = modules[4].split('&')
                        if 1 < len(vals) < 4:
                            undisk = kvm_cgroup.kvmDiskLimit(vals[0])
                            if vals[1].equal('read'):
                                if len(vals) == 3:
                                    undisk.diskreadunset(vals[2])
                                else:
                                    undisk.diskreadunset()
                            if vals[1].equal('write'):
                                if len(vals) == 3:
                                    undisk.diskreadunset(vals[2])
                                else:
                                    undisk.diskreadunset()
                    else:
                        self.send_error(404, "api not found")
                    
            elif modules[1].equal('docker'):
                if modules[2].equal('cpu'):
                    if modules[3].equal('set'):
                        vals = modules[4].split("&")
                        if len(vals) == 2:
                            cpu = docker_cgroup.dockerCpuLimit(vals[0])
                            cpu.cpulimit(vals(1))
                    elif modules[3].equal('unset'):
                        uncpu = docker_cgroup.dockerCpuLimit(modules[4])
                        uncpu.cpuunset()
                    else:
                        self.send_error(404, "api not found")
                elif modules[2].equal('cpuset'):
                    if modules[3].equal('set'):
                        vals = modules[4].split("&")
                        if len(vals) == 2:
                            cpuset = docker_cgroup.dockerCpusetLimit(vals[0])
                            cpuset.cpusetlimit(vals(1))
                    elif modules[3].equal('unset'):
                        uncpuset = docker_cgroup.dockerCpusetLimit(modules[4])
                        uncpuset.cpusetunset()
                    else:
                        self.send_error(404, "api not found")
                elif modules[2].equal('memory'):
                    if modules[3].equal('set'):
                        vals = modules[4].split("&")
                        if len(vals) == 2:
                            mem = docker_cgroup.dockerMemLimit(vals[0])
                            mem.memlimit(vals(1))
                    elif modules[3].equal('unset'):
                        unmem = docker_cgroup.dockerMemLimit(modules[4])
                        unmem.memunset()
                    else:
                        self.send_error(404, "api not found")
                elif modules[2].equal('blk_io'):
                    if modules[3].equal('set'):
                        vals = modules[4].split("&")
                        if 2 < len(vals) < 5:
                            disk = docker_cgroup.dockerDiskLimit(vals[0])
                            if vals[1].equal('read'):
                                if len(vals)== 3:
                                    disk.diskreadlimit(vals[3])
                                else:
                                    disk.diskreadlimit(vals[3],vals[4])
                                disk.diskreadlimit(vals[3])
                            elif vals[1].equal('write'):
                                if len(vals) == 3:
                                    disk.diskwritelimit(vals[3])  
                                else:
                                    disk.diskwritelimit(vals[3], vals[4])
                    elif modules[3].equal('unset'):
                        vals = modules[4].split('&')
                        if 1 < len(vals) < 4:
                            undisk = docker_cgroup.dockerDiskLimit(vals[0])
                            if vals[1].equal('read'):
                                if len(vals) == 3:
                                    undisk.diskreadunset(vals[2])
                                else:
                                    undisk.diskreadunset()
                            if vals[1].equal('write'):
                                if len(vals) == 3:
                                    undisk.diskreadunset(vals[2])
                                else:
                                    undisk.diskreadunset()
                    else:
                        self.send_error(404, "api not found")
            elif modules[1].equal('net'):
                serverpath = os.path.dirname(os.path.realpath(__file__))
                if len(modules == 3):
                    vals = modules[2].split("&")
                    if len(vals) == 4:
                        output = subprocess.Popen(serverpath+'/tcscript.sh', vals ,shell= True, stdout= subprocess.PIPE)
                    else:
                        self.send_error(404, "api not found")
            self.send_response(200)
            self.send_header('Content-type', contentType)
            self.end_headers()
            if output:
                self.wfile.write(output)
            else:
                self.wfile.write("OK")
        except IOError:
            self.send_error(404, 'Filf Not Found')
if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 12345), MainHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
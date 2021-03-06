import subprocess
from time import time


class Solution:
    def __init__(self):
        self.att_count = []
        self.blocked_addresses = []

    def block_address(self, source_ip):
        if source_ip in self.blocked_addresses:
            return 0
        p = subprocess.Popen(["iptables", "-t", "filter", "-A", "OUTPUT", "-d", "{}".format(source_ip), "-m", "comment", "--comment", "{}".format(time()), "-j", "DROP"],
                              stdout=subprocess.PIPE)
        output, err = p.communicate()
        print("Address {} blocked".format(source_ip))
        self.blocked_addresses.append(source_ip)
        return source_ip

    def block_after_count(self, source_ip):
        now = time()
        self.att_count = [[a, b, c] for [a, b, c] in self.att_count if now-b < 60]  #Deleting old data
        for sublist in self.att_count:
            if sublist[0] == source_ip:
                if sublist[2] > 4:
                    return self.block_address(source_ip)
                else:
                    sublist[2] += sublist[2]
                    return 0
        self.att_count.append([source_ip, now, 1])
        return 0

    def delete_files(self):
        pass

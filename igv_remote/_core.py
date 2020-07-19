#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core wrappers for send command
"""
import socket
import os


def _append_id(filename, id):
    return "{0}_{2}.{1}".format(*filename.rsplit('.', 1) + [id])
        
        
class IGV_remote:
    sock=None
    
    def __init__(self, 
                 squish = True, collapse = False, viewaspairs = False,
                 sort="base"):
        if self.sock:
            self.sock.close()
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._set_viewopts(squish, collapse, viewaspairs, sort) 
        # the view params are set during initialization
    
    def _set_saveopts(self, img_dir, img_basename, img_init_id=0) :
        # check if path is absolute and exits
        if not os.path.exists(img_dir):
            print("Initializing a directory called {} in current dir".format(img_dir))
            os.mkdir(img_dir)
        img_fulldir = os.path.abspath(img_dir)
        
        # check if the image name has proper extension
        accepted_extensions = ["png", "svg", "jpg"]
        if not any(x in img_basename for x in accepted_extensions):
            raise Exception("filename has to contain extension, one of jpg/svg/png")
        
        self._img_fulldir = img_fulldir
        self._img_basename = img_basename
        self._img_id = img_init_id
    
    def _set_viewopts(self, squish, collapse, viewaspairs, sort):
        self._squish = squish
        self._collapse = collapse
        self._viewaspairs = viewaspairs
        self._sort = sort

    def _connect(self, host="127.0.0.1", port=60151):
        self.sock.connect((host, port))
        print("socket initialized")
    
    def _new(self):
        self._send("new ")

    def _send(self, cmd):
        s = self.sock
        cmd = cmd + '\n'
        s.send(cmd.encode('utf-8'))
        return s.recv(2000).decode('utf-8').rstrip('\n')
    
    def _load(self, *urls):
        print(urls)
        # self._send("new ")
        if len(urls) < 1:
            raise Exception("Please provide at least one URL to load")
        for url in urls:
            self._send("load %s" % url)
            self._adjust_viewopts()


    def _adjust_viewopts(self):
        # specify view options
        if self._squish:
            self._send( "squish ")
        if self._collapse:
            self._send( "collapse ")
        if self._viewaspairs:
            self._send( "viewaspairs ")
        self._send( "sort {}".format(self._sort))
    
    
    
    def _goto(self, 
             chromosome=None, pos=None, end_pos=None):
        """
        Note that the position params could be either list or single element.
        examples: chromosome=2, start_pos=[34,3890,34859], end_pos = [3544, 6909, 34980]
        """
        
        if end_pos is None:
            
            start_pos = pos-1
            end_pos = start_pos+2
            #position = "chr{chr}:{pos}".format(chr=chromosome, pos=pos)
        elif start_pos and end_pos:
            start_pos ='{:,}'.format(start_pos)
            end_pos = '{:,}'.format(end_pos)
            
        else:
            raise Exception("No view location specified")
        
        position= 'chr{}:{}-{}'.format(chromosome,start_pos, end_pos)
                    print("position to view:", position)

        self._send( "goto %s" % position)
        self._adjust_viewopts()
        

    def _snapshot(self):
        self._send( "snapshotDirectory %s" % self._img_fulldir)
        newname = _append_id(self._img_basename, self._img_id)
        self._send( "snapshot %s" % newname)
        self._img_id += 1

    def _close(self):
        self.sock.close()

ir = IGV_remote()
connect = ir._connect
set_viewopts = ir._set_viewopts
set_saveopts = ir._set_saveopts
goto = ir._goto
load = ir._load
send = ir._send
close = ir._close
new = ir._new
snapshot = ir._snapshot

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core wrappers for send command
"""
import socket
import os


def _append_id(filename, id):
    return "{0}_{2}.{1}".format(*filename.rsplit('.', 1) + [id])

def _parse_loc(chromosome, pos1, pos2=None, expand=20):
    if expand < 20:
        print("IGV expands left and right margin by at least 20bp")
        expand=20
    start_pos = int(pos1-expand)
    if pos2 is None:
        end_pos = int(pos1+expand)
    else:
        end_pos = int(pos2)
    start_pos ='{:,}'.format(int(start_pos))
    end_pos = '{:,}'.format(int(end_pos))
    position= 'chr{}:{}-{}'.format(int(chromosome),start_pos, end_pos)
    print("Position to view: {}".format(position))
    return position
        
class IGV_remote:
    sock=None
    
    def __init__(self, 
                 view_type="collapsed", viewaspairs = False,
                 sort="base"):
        if self.sock:
            self.sock.close()
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._set_viewopts(view_type, viewaspairs, sort) 
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
    
    def _set_viewopts(self, view_type, viewaspairs, sort):
        if view_type not in ['squished', 'collapsed', 'expanded']:
            raise Exception("view_type must be one of [squished, collapsed, expanded]")
        self._view_type = view_type
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
        if self._view_type == "squished":
            self._send( "squish ")
        elif self._view_type == "collapsed":
            self._send( "collapse ")
        elif self._view_type == "expanded":
            self._send("expand ")
        else:
            print("view_type other than squished/collapsed/expanded cannot be understood, will use expand")
            self._send("expand ")

        if self._viewaspairs:
            self._send( "viewaspairs ")
        self._send( "sort {}".format(self._sort))
    
    def _goto(self, 
             chromosome=None, pos1=None, pos2=None, expand=20):

        position = _parse_loc(chromosome, pos1, pos2, expand)
        print("position to view:", position)

        self._send( "goto %s" % position)
    
    def _goto_multiple(self, expand=20, **loci):
        """
        goto_multiple(expand=20, chr1=<seqname of first panel>, chr2=<seqname of second panel>, pos1=<position of first panel>, pos2=<position of second panel>)
        """
        self._send("goto {} {}".format(_parse_loc(loci['chr1'], loci['pos1'], None, expand),  _parse_loc(loci['chr2'], loci['pos2'], None, expand)))

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
goto_multiple = ir._goto_multiple
snapshot = ir._snapshot

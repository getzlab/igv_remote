#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core wrappers for send command
"""
import socket
import os
import re

def _append_id(filename, id):
    return "{0}_{2}.{1}".format(*filename.rsplit('.', 1) + [id])

VALID_VIEW_OPTS = ['squish', 'collapse', 'expand']

class IGV_remote:

    def __init__(self, host="127.0.0.1", port=60151, view_type='collapse', sort='base', verbose=True, recv_timeout=60):
        self.set_viewopts(view_type,  sort)
        self.HOST = host
        self.PORT = port

        self.verboseprint = print if verbose else lambda *a, **k: None
        self.recv_timeout = recv_timeout # time to wait for a response from IGV before exiting (seconds)

    def set_viewopts(self, view_type,  sort):
        if view_type not in VALID_VIEW_OPTS:
            raise ValueError(f"view_type must be one of {VALID_VIEW_OPTS}. Input was {view_type}")
        self._view_type = view_type
        self._sort = sort

    def set_saveopts(self, img_dir, img_basename, img_init_id=0) :
        # check if path is absolute and exits
        if not os.path.exists(img_dir):
            print("Initializing a directory called {} in current dir".format(img_dir))
            os.mkdir(img_dir)
        img_fulldir = os.path.abspath(img_dir)
        print("Snapshots are available in {}".format(img_fulldir))
        # check if the image name has proper extension
        accepted_extensions = ["png", "svg", "jpg"]
        if not any(x in img_basename for x in accepted_extensions):
            raise ValueError("filename has to contain extension, one of jpg/svg/png")
        
        self._img_fulldir = img_fulldir
        self._img_basename = img_basename
        self._img_id = img_init_id
        
    def send_cmds(self, cmds):
        for cmd in cmds:
            self._send_cmd(cmd)

    def _send_cmd(self, cmd, timeout=20):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        
        format_cmd = f'{cmd} \n'.encode('utf-8')
        self.verboseprint(f"sending command: {format_cmd}")
        self.socket.send(format_cmd)

        self.socket.settimeout(timeout) # if IGV times out, we recommend you restart IGV
        self.verboseprint(self.socket.recv(4096))
        
        self.socket.close()

    def new(self):
        self._send_cmd('new')

    def load(self, *urls):
        self.verboseprint(urls)

        if len(urls) < 1:
            raise ValueError("Please provide at least one URL to load")
        for url in urls:
            self._send_cmd("load %s" % url)
            self._adjust_viewopts()

    def _parse_loc(self, chromosome, pos1, pos2=None, expand=20):
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
        position= '{}:{}-{}'.format(chromosome, start_pos, end_pos)
        self.verboseprint("Position to view: {}".format(position))
        return position

    def goto(self, chromosome, start_pos, end_pos=None, expand=20):
        """
        if only start_pos is supplied, we will expand view range by 'expand' parameter
        """

        position = self._parse_loc(chromosome, start_pos, end_pos, expand)
        self._send_cmd( "goto %s" % position)
        # make sure viewopts are preserved
        self._adjust_viewopts()
    
    def goto_multiple(self, expand=20, **kwargs):
        """
        goto_multiple(expand=20, chr1=<seqname of first panel>, chr2=<seqname of second panel>, pos1=<position of first panel>, pos2=<position of second panel>)
        """
        chrpos = { "chr" : {}, "pos" : {} }
        try:
            for k, v in kwargs.items():
                arg = re.match(r'^(chr|pos)(\d+)$', k)
                if arg is not None:
                    chrpos[arg.group(1)][arg.group(2)] = v
                else:
                    raise Exception
            if chrpos["chr"].keys() != chrpos["pos"].keys():
                raise Exception
        except:
            raise ValueError("When specifying multiple loci, arguments must be of the format chr1 = <chr1>, pos1 = <pos1>, ..., chrN = <chrN>, posN = <posN>")
        
        positions = []
        for (_, chrv), (_, posv) in zip(chrpos['chr'].items(), chrpos['pos'].items()):
            positions.append(self._parse_loc(chrv, posv, None, expand))
        self._send_cmd("goto {}".format(" ".join(positions)))
        # make sure viewopts are preserved
        self._adjust_viewopts()

    def snapshot(self): # snapshot as-is
        assert self._img_fulldir is not None, "Please set view optins with ir.set_saveopts() first"
        self._send_cmd( "snapshotDirectory %s" % self._img_fulldir)
        newname = _append_id(self._img_basename, self._img_id)
        self._send_cmd( "snapshot %s" % newname)
        self._img_id += 1

    def _adjust_viewopts(self):
        self._send_cmd(f"{self._view_type}")
        self._send_cmd(f"sort {self._sort}")


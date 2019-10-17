#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:20:22 2019

An potential naive attempt to automate 
1. paired/single bam url submission
2. take snapshot for specified regions
within python using TCP sockets.

@author: qingzhang
"""
import socket
import os


def _append_id(filename, id):
    return "{0}_{2}.{1}".format(*filename.rsplit('.', 1) + [id])

def _parse_loc(chromosome, start_pos, end_pos):
    """
    A helper function to parse location specifiers to list of tuples
    """
    # change both start and end to list
    if type(start_pos) != list:
        start_pos = [start_pos]
    if end_pos == None:
        end_pos = [x+1 for x in start_pos]
    if type(end_pos) != list:
        end_pos = [end_pos]
        
    # repeat either list
    if len(start_pos) != len(end_pos):
        if len(start_pos) == 1:
            start_pos = start_pos*len(end_pos)
        elif len(end_pos) == 1:
            end_pos = end_pos*len(start_pos)
        else:
            raise ValueError("positions (chromosome and pos) must match in size")
        
    # for mat chr to list
    if type(chromosome) != list:
        chromosome = [chromosome]
    if len(chromosome) == 1:
        chromosome = chromosome*len(start_pos)
    
    # check position length
    if (len(chromosome) != len(end_pos) or len(chromosome) != len(start_pos)):
        raise ValueError("positions (chromosome and pos) must match in size")
            
    # get the list of tuples as input
    positions = list(zip(chromosome, start_pos, end_pos))
    return(positions)
        
        
class IGV_remote:
    sock=None
    img_fulldir ="/tmp/igv-snapshots"
    
    def __init__(self, 
                 squish = True, collapse = False, viewaspairs = False):
        if self.sock:
            self.sock.close()
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._set_viewopts(squish, collapse, viewaspairs)
    
    def _set_saveopts(self, img_fulldir, img_basename ):
        # check if path is absolute and exits
        if not os.path.exists(img_fulldir):
            raise Exception("cannot locate diretory, please make sure it exists")
        if not os.path.isabs(img_fulldir):
            raise Exception("please specify absolute path, not relative")
        
        # check if the image name has proper extension
        accepted_extensions = ["png", "svg", "jpg"]
        if not any(x in img_basename for x in accepted_extensions):
            raise Exception("filename has to contain extension, one of jpg/svg/png")
        
        self._img_fulldir = img_fulldir
        self._img_basename = img_basename
    
    def _set_viewopts(self, squish, collapse, viewaspairs):
        self._squish = squish
        self._collapse = collapse
        self._viewaspairs = viewaspairs

    def _connect(self, host="127.0.0.1", port=60151):
        self.sock.connect((host, port))
        print("socket initialized")
    
    def _send(self, cmd):
        s = self.sock
        cmd = cmd + '\n'
        s.send(cmd.encode('utf-8'))
        return s.recv(2000).decode('utf-8').rstrip('\n')
    
    def _load(self, url1, url2=None):
        self._send("load %s" % url1)
        if url2:
            self._send("load %s" % url2)

    def _goto(self, 
             chromosome=None, start_pos=None, end_pos=None):
        """
        Note that the position params could be either list or single element.
        examples: chromosome=2, start_pos=[34,3890,34859], end_pos = [3544, 6909, 34980]
        """
        if (not end_pos) and start_pos:
            end_pos = start_pos+1
        if start_pos and end_pos:
            start_pos ='{:,}'.format(start_pos)
            end_pos = '{:,}'.format(end_pos)
            position= 'chr{}:{}-{}'.format(chromosome,start_pos, end_pos)
            print("position to view:", position)
        else: 
            raise Exception("No view location specified")
        self._send( "goto %s" % position)


    def _load_snap(self, url1, url2 = None, 
                chromosome=None, start_pos=None, end_pos=None):
        """
        <s> is the socket we initialized
        <url> is a gs url for your interested bam file
        <chromosome> is a number or a list
        <start_pos> is a number in unit of bp, so as the end_pos, 
        can also be a list of numbers
        ## <genesymbol> is no longer accepted as valid input!
        can also be a list of symbols,
        user need either chromosome input or gene input, 
        otherwise will be error
        <imgdir> is the path where you want to save the snapshots
        need to be FULLPATH!
        <imgname> is the name of our saved plot - acceptable file types are 
        .png, .jpg, or .svg
        """
            
        self._send( "new ")
        self._load(*(url1, url2))
        
        # get locations as list of tuples
        positions = _parse_loc(chromosome, start_pos, end_pos)
        # -------- plot --------
        for i, position in enumerate(positions):
            self._goto(*position)
            
            if self._squish:
                self._send( "squish ")
            if self._collapse:
                self._send( "collapse ")
            if self._viewaspairs:
                self._send( "viewaspairs ")
            self._send( "snapshotDirectory %s" % self._img_fulldir)
            if self._img_basename!=None:
                newname = _append_id(self._img_basename, i)
                self._send( "snapshot %s" % newname)
            else: 
                self._send( "snapshot %s" % self._img_basename)
            
    
    def _close(self):
        self.sock.close()

ir = IGV_remote()
connect = ir._connect
set_viewopts = ir._set_viewopts
set_saveopts = ir._set_saveopts
goto = ir._goto
load = ir._load
load_snap = ir._load_snap
send = ir._send
close = ir._close

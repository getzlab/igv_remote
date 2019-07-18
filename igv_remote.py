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



def init(host="127.0.0.1", port=60151):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("socket initialized")
    return(s)

def send(s, cmd):
    cmd = cmd + '\n'
    s.send(cmd.encode('utf-8'))
    return s.recv(2000).decode('utf-8').rstrip('\n')


def goto(s, 
         chromosome=None, start_pos=None, end_pos=None):
    """
    Note that the position params could be either list or single element.
    A list of ch
    """
    if start_pos and end_pos:
        start_pos ='{:,}'.format(start_pos)
        end_pos = '{:,}'.format(end_pos)
        position= 'chr{}:{}-{}'.format(chromosome,start_pos, end_pos)
        print("position to view:", position)
    else: 
        raise Exception("No view location specified")
        return -1
    send(s, "goto %s" % position)

def append_id(filename, id):
    return "{0}_{2}.{1}".format(*filename.rsplit('.', 1) + [id])

# a helper function to get chr ranges as list of tuple (chr, start, end)
def parse_loc(chromosome, start_pos, end_pos):
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


def load_single(s, url, 
                chromosome=None, start_pos=None, end_pos=None,  
                imgfulldir="/home/qing/igv_snapshots",imgname="testsingle.png", 
                squish=True, collapse=False, viewaspairs=False):
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
        
        send(s, "new ")
        send(s, "load %s" % url)
        
        # get locations as list of tuples
        positions = parse_loc(chromosome, start_pos, end_pos)
        # -------- plot --------
        for i, position in enumerate(positions):
            goto(s, *position)
            
            if squish:
                send(s, "squish ")
            if collapse:
                send(s, "collapse ")
            if viewaspairs:
                send(s, "viewaspairs ")
            send(s, "snapshotDirectory %s" % imgfulldir)
            if imgname!=None:
                newname = append_id(imgname, i)
                send(s, "snapshot %s" % newname)
            else: 
                send(s, "snapshot %s" % imgname)
            

def load_pair(s, tumor_bam, normal_bam, 
              chromosome=None, start_pos=None, end_pos=None,  
              imgfulldir="/home/qing/igv_snapshots", imgname="testpair.png", 
              squish=True, collapse=False, viewaspairs=False):
        """
        <s> is the socket we initialized
        <tumor_bam> is a gs url for your interested tumor bam file
        <normal_bam> is a gs url for your interested normal bam file
        <chromosome> is a number
        <start_pos> is a number in unit of bp, so as the end_pos
         ## note that we no longer accept gene symbol as input
        <imgdir> is the path where you want to save the snapshots
        need to be FULLPATH!
        <imgname> is the name of our saved plot - acceptable file types are 
        .png, .jpg, or .svg
        """        
        # initialize pair view
        send(s, "new ")

        send(s, "load %s" % tumor_bam)
        send(s, "load %s" % normal_bam)
            
        # get the list of tuples as input
        positions = parse_loc(chromosome, start_pos, end_pos)
        
        # -------- plot --------
        for i, position in enumerate(positions):
            goto(s, *position)
            
            if squish:
                send(s, "squish ")
            if collapse:
                send(s, "collapse ")
            if viewaspairs:
                send(s, "viewaspairs ")
            send(s, "snapshotDirectory %s" % imgfulldir)
            if imgname!=None:
                newname = append_id(imgname, i)
                send(s, "snapshot %s" % newname)
            else: 
                send(s, "snapshot %s" % imgname)
    

def close(s):
    s.close()

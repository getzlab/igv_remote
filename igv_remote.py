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

def load_single(s, url, 
                chromosome=None, start_pos=None, end_pos=None, genesymbol=None,  
                imgfulldir="/home/qing/igv_snapshots", imgname="testsingle.png", 
                squish=True, collapse=False):
        """
        <s> is the socket we initialized
        <url> is a gs url for your interested bam file
        <chromosome> is a number
        <start_pos> is a number in unit of bp, so as the end_pos
        <genesymbol> is the genesymbol used to locate the view
        user need either chromosome input or gene input, 
        otherwise will have error
        <imgdir> is the path where you want to save the snapshots
        need to be FULLPATH!
        <imgname> is the name of our saved plot - acceptable file types are 
        .png, .jpg, or .svg
        """
        if start_pos and end_pos:
            start_pos ='{:,}'.format(start_pos)
            end_pos = '{:,}'.format(end_pos)
            position= 'chr{}:{}-{}'.format(chromosome,start_pos, end_pos)
            print("position to view:", position)
        elif genesymbol:
            position=genesymbol
            print("gene to view:", position)
        else: 
            print("No view location specified!")
            return None
        send(s, "new ")
        send(s, "load %s" % url)
        send(s, 'goto %s' % position)
        if squish:
            send(s, "squish ")
        if collapse:
            send(s, "collapse ")
        send(s, "snapshotDirectory %s" % imgfulldir)
        send(s, "snapshot %s" % imgname)

def load_pair(s, tumor_bam, normal_bam, 
              chromosome=None, start_pos=None, end_pos=None, genesymbol=None,  
              imgfulldir="/home/qing/igv_snapshots", imgname="testpair.png", 
              squish=True, collapse=False):
        """
        <s> is the socket we initialized
        <tumor_bam> is a gs url for your interested tumor bam file
        <normal_bam> is a gs url for your interested normal bam file
        <chromosome> is a number
        <start_pos> is a number in unit of bp, so as the end_pos
        <genesymbol> is the genesymbol used to locate the view
        user need either chromosome input or gene input, 
        otherwise will have error
        <imgdir> is the path where you want to save the snapshots
        need to be FULLPATH!
        <imgname> is the name of our saved plot - acceptable file types are 
        .png, .jpg, or .svg
        """
        # define position
        if start_pos and end_pos:
            start_pos = '{:,}'.format(start_pos)
            end_pos = '{:,}'.format(end_pos)
            position= 'chr{}:{}-{}'.format(chromosome,start_pos, end_pos)
            print("position to view:", position)
        elif genesymbol:
            position=genesymbol
            print("gene to view:", position)
        else: 
            print("No view location specified!")
            return None
        
        # initialize pair view
        send(s, "new ")
        send(s, "viewaspairs ")
        send(s, "load %s" % tumor_bam)
        send(s, "load %s" % normal_bam)
        send(s, "goto %s" % position)
        if squish:
            send(s, "squish ")
        if collapse:
            send(s, "collapse ")
        send(s, "snapshotDirectory %s" % imgfulldir)
        send(s, "snapshot %s" % imgname)

def close(s):
    s.close()

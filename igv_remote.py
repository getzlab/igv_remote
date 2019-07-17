#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 18:04:19 2019
An potential naive attempt to automate 
1. paired/single bam url submission
2. take snapshot for specified regions
within python using sockets.

@author: qingzhang
"""
import sys
import os
import socket
import os.path as op



class igv:
    _socket = None
    _path = None
    
    def __init__(self, host="127.0.0.1", port=60151, imgdir="/tmp/igv_remote"):
        self.host = socket.gethostname()
        self.port = port
        self.commands = []
        self.connect()
        self.set_path(imgdir)
        
    def connect(self):
        if self._socket:
            self._socket.close()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))
        
    def send(self, cmd):
        # socket in Python2 oprates with strings
        if sys.version_info.major == 2:
            self._socket.send(cmd + '\n')
            return self._socket.recv(4096).rstrip('\n')
        # while socket in Python3 requires bytes
        else:
            self.commands.append(cmd)
            cmd = cmd + '\n'
            self._socket.send(cmd.encode('utf-8'))
            return self._socket.recv(4096).decode('utf-8').rstrip('\n')
    
    def set_path(self, imgdir):
        if imgdir == self._path:
            return
        if not op.exists(imgdir):
            os.makedirs(imgdir)

        self.send('snapshotDirectory %s' % imgdir)
        self._path = imgdir
    
#    def loadpair(self, df, chromosome, start_pos, end_pos, genesymbol, imgname, squish=True):
#        """
#        df is a pandas pivot dataframe containing column for 
#        "sample_id", "tumorBAM" and "normalBAM". The last two
#        columns are urls pointing to the bam files. Please refer
#        to the example data in "testdf.tsv" for more information.
#        
#        The code to generate such dataframe from dalmatian can 
#        be found in gendf.py
#        
#        The function will output the snapshot images with the 
#        two bam loaded under selected chromosome region to 
#        the specified directory
#        """
#        df = df.dropna()
#        # fixme: add colname check
#        dfcols = df.columns.tolist()
#        # genenrate customized position input, from either gene/chrpos
#        if start_pos & end_pos:
#            start_pos = f'{start_pos:,}'
#            end_pos = f'{end_pos:,}'
#            position= 'chr{}:{}-{}'.format(chromosome,start_pos, end_pos)
#            print("position to view:", position)
#        elif genesymbol:
#            position=genesymbol
#        
#        # go to view
#        if "tumor" in dfcols[0] & "normal" in dfcols[1]:
#            self.send("new ")
#            for i in range(df.shape[0]):
#                self.send("viewaspairs ")
#                tumor_bam = df.iloc[i,0] # choose the first column
#                self.send("load ", tumor_bam)
#                normal_bam = df.iloc[i,1] # choose the second column
#                self.send("load ", normal_bam)
#                self.send('goto ', position)
#                if squish:
#                    self.send("squish ")
#                self.send("snapshot ", imgname)
#        else: 
#            print("""
#                  dataframe column 1 should contain tumor, 
#                  and column name 2 should contain normal
#                  """)
#            return
        
    def load_single(self, url, 
                    chromosome=None, start_pos=None, end_pos=None, genesymbol=None,  
                    imgname="testsingle.png", squish=True):
        """
        input url is a gs url for your interested bam file
        chromosome is a number
        start_pos is a number in unit of bp, so as the end_pos
        genesymbol is the genesymbol used to locate the view
        user need either chromosome input or gene input, 
        otherwise will have error
        """
        if start_pos and end_pos:
            start_pos ='{:,}'.format(start_pos)
            end_pos = '{:,}'.format(end_pos)
            position= 'chr{}:{}-{}'.format(chromosome,start_pos, end_pos)
            print("position to view:", position)
        elif genesymbol:
            position=genesymbol
        else: 
            print("No view location specified!")
            return None
        self.send("new ")
        self.send("load %s" % url)
        self.send('goto %s' % position)
        if squish:
            self.send("squish ")
        self.send("snapshot %s" % imgname)
        
    def load_pair(self, tumor_bam, normal_bam, 
                  chromosome=None, start_pos=None, end_pos=None, genesymbol=None,  
                  imgname="testpaired.png", squish=True):
        # define position
        if start_pos and end_pos:
            start_pos = '{:,}'.format(start_pos)
            end_pos = '{:,}'.format(end_pos)
            position= 'chr{}:{}-{}'.format(chromosome,start_pos, end_pos)
            print("position to view:", position)
        elif genesymbol:
            position=genesymbol
        else: 
            print("No view location specified!")
            return None
        
        # initialize pair view
        self.send("new ")
        self.send("viewaspairs ")
        self.send("load %s" % tumor_bam)
        self.send("load %s" % normal_bam)
        self.send("goto %s" % position)
        if squish:
            self.send("squish ")
        self.send("snapshot %s" % imgname)
            
#
#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()



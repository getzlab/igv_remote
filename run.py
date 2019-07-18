#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:20:05 2019

a brief example

@author: qingzhang
"""

import igv_remote
import pandas as pd

testdf = pd.read_csv("test_df.csv")

# initialize the socket
igv_remote.connect()

# set some view/save params
igv_remote.set_saveopts(img_fulldir = "/home/qing/igv_snapshots/", img_basename = "test.png" ) # must be set!
igv_remote.set_viewopts(collapse = False, squish = True, viewaspairs = True ) # optional

# single bam snapshots
sample_gspath = "gs://5aa919de-0aa0-43ec-9ec3-288481102b6d/tcga/ACC/DNA/WXS/BI/ILLUMINA/TCGA_MC3.TCGA-PK-A5HA-10A-01D-A29L-10.bam"
igv_remote.load_single(sample_gspath, 
            chromosome = 12, start_pos = [23853, 45728, 352884])
print("single bam view generated")

# paired bam snapshots
tumor_gspath = testdf["NB"][0]
normal_gspath = testdf["TP"][0]
igv_remote.load_pair(tumor_bam=tumor_gspath, normal_bam=normal_gspath, 
          chromosome = 12, start_pos = [23853, 45728, 352884])
print("paired bam view generated")
igv_remote.close()

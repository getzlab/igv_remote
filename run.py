#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:20:05 2019

a brief example

@author: qingzhang
"""

import igv_remote

# initialize the socket
igv_remote.connect()

# set some view/save params
igv_remote.set_saveopts(img_fulldir = "/home/qing/igv_snapshots/", img_basename = "test.png" ) # must be set!
igv_remote.set_viewopts(collapse = False, squish = True, viewaspairs = True, sort="base" ) # optional

# single bam snapshots
sample_gspath = "gs://5aa919de-0aa0-43ec-9ec3-288481102b6d/tcga/ACC/DNA/WXS/BI/ILLUMINA/TCGA_MC3.TCGA-PK-A5HA-10A-01D-A29L-10.bam"
igv_remote.load_snap(sample_gspath, 
            chromosome = 12, start_pos = [23853, 45728, 352884])
print("single bam view generated")

# paired bam snapshots
normal_gspath = "gs://5aa919de-0aa0-43ec-9ec3-288481102b6d/tcga/ACC/DNA/WXS/BI/ILLUMINA/TCGA_MC3.TCGA-OR-A5J1-10A-01D-A29L-10.bam"
tumor_gspath = "gs://5aa919de-0aa0-43ec-9ec3-288481102b6d/tcga/ACC/DNA/WXS/BI/ILLUMINA/TCGA_MC3.TCGA-OR-A5J1-01A-11D-A29I-10.bam"
igv_remote.load_snap(tumor_gspath, normal_gspath, 
          chromosome = 12, start_pos = [23853, 45728, 352884])
print("paired bam view generated")
igv_remote.close()

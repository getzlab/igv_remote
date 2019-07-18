#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:20:05 2019

@author: qingzhang
"""

import igv_remote
import pandas as pd

testdf = pd.read_csv("test_df.csv")


# initialize igv port
# Note: you need to have IGV started on VM(?)
sock = igv_remote.init()

# test igv with single url
sample_gspath = "gs://5aa919de-0aa0-43ec-9ec3-288481102b6d/tcga/ACC/DNA/WXS/BI/ILLUMINA/TCGA_MC3.TCGA-PK-A5HA-10A-01D-A29L-10.bam"
igv_remote.load_single(sock, sample_gspath, 
                       chromosome = 12, start_pos = [23853, 45728, 352884], 
                       end_pos = 352889, imgname="testsingle.png")
print("single bam view generated")

# test igv with paired url
tumor_gspath = testdf["NB"][0]
normal_gspath = testdf["TP"][0]
igv_remote.load_pair(sock, tumor_bam=tumor_gspath, normal_bam=normal_gspath, 
                     chromosome = 12, start_pos = [23853, 45728, 352884], 
                     end_pos = 352889, imgname="testpair.png")
print("paired view generated")

igv_remote.close(sock)



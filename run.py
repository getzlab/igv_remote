#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 01:15:56 2019

A sample script to run igv_remote utils

@author: qingzhang
"""
import igv_remote
import pandas as pd

testdf = pd.read_csv("test_df.csv")

# init
igv = igv_remote.igv(imgdir="igv-snapshots/")
print("socket initialized!")

# test igv with single url
sample_gspath = "gs://5aa919de-0aa0-43ec-9ec3-288481102b6d/tcga/ACC/DNA/WXS/BI/ILLUMINA/TCGA_MC3.TCGA-PK-A5HA-10A-01D-A29L-10.bam"
igv.load_single(sample_gspath, genesymbol="TP53", imgname="testsingle.png")
print("single bam view generated!")

# test igv with paired url
tumor_gspath = testdf["NB"][0]
normal_gspath = testdf["TP"][0]
igv.load_pair(tumor_bam=tumor_gspath, normal_bam=normal_gspath, genesymbol="TP53", imgname="testpair.png")
print("paired view generated!")


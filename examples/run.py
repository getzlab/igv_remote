#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example showing snapshot functionalities for multiple bams
"""

import igv_remote as ir

# initialize the socket
ir.connect()

# set some view/save params
ir.set_saveopts(img_dir = "igv_snapshots/", img_basename = "test.png" ) # must be set!
ir.set_viewopts(collapse = False, squish = True, viewaspairs = True, sort = "base" ) # optional

# single bam snapshots
sample_gspath = "gs://..."
ir.new()
ir.goto(12, 25398284)
ir.load(sample_gspath)
ir.snapshot()
print("single bam view generated")

# paired bam snapshots
tumor_gspath = "gs://..."
normal_gspath= "gs://..."


ir.new()
ir.goto(12, 25398284)
ir.load(tumor_gspath, normal_gspath)
ir.snapshot()
print("paired bam view generated")



ir.close()

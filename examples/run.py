#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example showing snapshot functionalities for multiple bams
"""

import igv_remote as ir

# initialize the socket
ir.connect()

# set some view/save params
# save options are needed only if you are taking snapshots
# the following config will allow you to save snapshots to '$(pwd)/igv_snapshots/test_0.png'
ir.set_saveopts(img_dir = "igv_snapshots/", img_basename = "test.png" ) 

# view options are used to configure the appearance of IGV, the defualt would be:
ir.set_viewopts(view_type = 'collapsed', sort = "base" ) # optional

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

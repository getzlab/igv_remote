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
sample_gspath = "gs://fc-6febaccc-27b7-46d0-8d3f-8b52922499f8/aba98162-67cd-45bc-81db-3b9ab5d92eec/picardRealignment_indel/b11d9f3d-ae51-4ffa-a1d1-e00ae52c5826/call-index_tumor/MMRF_1078tumor.cleaned.bam"

ir.new()
ir.goto(12, 25398284)
ir.load(sample_gspath)
# ir.snapshot()
print("single bam view generated")

# paired bam snapshots
normal_gspath = "gs://fc-6febaccc-27b7-46d0-8d3f-8b52922499f8/aba98162-67cd-45bc-81db-3b9ab5d92eec/picardRealignment_indel/b11d9f3d-ae51-4ffa-a1d1-e00ae52c5826/call-index_tumor/MMRF_1078tumor.cleaned.bam"
tumor_gspath = "gs://fc-6febaccc-27b7-46d0-8d3f-8b52922499f8/aba98162-67cd-45bc-81db-3b9ab5d92eec/picardRealignment_indel/b11d9f3d-ae51-4ffa-a1d1-e00ae52c5826/call-index_normal/MMRF_1078normal.cleaned.bam"

ir.new()
ir.goto(12, 25398284)
ir.load(tumor_gspath, normal_gspath)
# ir.snapshot()
print("paired bam view generated")



igv_remote.close()

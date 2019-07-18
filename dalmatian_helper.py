#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:41:41 2019

A potentially naive attempt to generate paired gspaths 
in a pd dataframe from Dalmatian

@author: qingzhang
"""
import re
import dalmatian #pip install dalmatian
import pandas as pd
import numpy as np


def re_match_wsname(ws_list, re_string="TCGA_([A-Z]+)_ControlledAccess.*"):
    r = re.compile(re_string)
    ltps = [(ws["workspace"]["namespace"], ws["workspace"]["name"]) for ws in ws_list if r.match(ws["workspace"]["name"])]
    return ltps


def get_pairs_from_wsname(www):
    paired_path = pd.DataFrame()
    for nspair in www:
        S = dalmatian.WorkspaceManager(*nspair).get_samples()
        
        sample_df = S.reset_index()["sample_id"].str.extract(r"([A-Z]+)-(..-....)-(..)$")
        path_df = S.reset_index()[["sample_id","WXS_bam_path"]]
        concat_df = pd.concat([sample_df, path_df], axis=1)
        concat_df.columns = ["cohort","id","type","sample_id","bam_path"]
        concat_df['pid'] = concat_df['cohort'].str.cat(concat_df['id'],sep="-")
        reset_df = pd.pivot_table(concat_df, 
                                  index=["pid"], columns=["type"], values=["bam_path"],
                                  aggfunc=np.sum).reset_index()
        paired_path = reset_df.rename_axis(None)["bam_path"]
        paired_path["pid"] = reset_df["pid"]
        paired_path = paired_path.append(pd.DataFrame(paired_path), ignore_index=True)
    return paired_path

# examples:
if False:
    ws_list = dalmatian.firecloud.api.list_workspaces().json()
    paired_path = get_pairs_from_wsname(re_match_wsname(ws_list))

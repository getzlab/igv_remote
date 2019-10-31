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
        print(paired_path.shape)
        # get sample info
        S = dalmatian.WorkspaceManager("/".join(nspair)).get_samples().reset_index()
        sample_df = pd.concat([S["sample_id"].str.extract(r"([A-Z]+)-(..-....)-(..)$"), S["WXS_bam_path"]], axis=1).dropna()
        sample_df.columns = ["cohort", "patient", "sample_type","bam_path"]

        # get pair info
        P = dalmatian.WorkspaceManager("/".join(nspair)).get_pair_sets().reset_index()
        P = P.loc[P["library_strategy"].str.contains("WXS"),"pairs"].tolist()[0]

        pair_df = pd.Series(P).str.extract(r"([A-Z]+)-(..-....)-(..)-(..)$")
        pair_df.columns = ["cohort", "patient", "tumor_type", "normal_type"]
        pair_expand = pd.melt(pair_df, id_vars = ["cohort","patient"], 
                value_vars=["tumor_type", "normal_type"],
                value_name = "sample_type").drop(columns="variable").dropna()

        # inner join
        path_dict = pd.merge(pair_expand, sample_df, how = "inner" )
        path_dict["file_name"] = path_dict.bam_path.apply(lambda x: re.findall("([^/]+$)", x)[0])
        path_dict["sample_type"] = path_dict.sample_type.apply(lambda x: "tumor" if x[0] == "T" else "normal")
        path_dict["pid"] = path_dict[['cohort', 'patient']].apply(lambda x: '-'.join(x), axis=1)

        paired_path = paired_path.append(path_dict)
    return paired_path


# examples:
if __name__ == "__main__":
    ws_list = dalmatian.firecloud.api.list_workspaces().json()
    wsname = re_match_wsname(ws_list)
    pp2 = get_pairs_from_wsname(wsname)
    pp2.to_csv("mpairs_update.csv")


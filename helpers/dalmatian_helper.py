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
        S = dalmatian.WorkspaceManager(*nspair).get_samples()
        
        sample_df = S.reset_index()["sample_id"].str.extract(r"([A-Z]+)-(..-....)-(..)$")
        path_df = S.reset_index()[["sample_id","WXS_bam_path"]]
        concat_df = pd.concat([sample_df, path_df], axis=1)
        concat_df.columns = ["cohort","id","type","sample_id","bam_path"]
        concat_df['pid'] = concat_df['cohort'].str.cat(concat_df['id'],sep="-")
        reset_df = pd.pivot_table(concat_df, 
                                  index=["pid"], columns=["type"], values=["bam_path"],
                                  aggfunc=np.sum).reset_index()
        new_paired_path = reset_df.rename_axis(None)["bam_path"]
        new_paired_path["pid"] = reset_df["pid"]
        paired_path = paired_path.append(pd.DataFrame(new_paired_path), 
                                         ignore_index=True, sort=True)
                                         #columns = ["pid","NB","NT","TR","TP"])
    return paired_path


def match_pair(paired_path):
    colnames = paired_path.columns.tolist()
    cols_we_care = ["NB", "NT", "TP", "TR"]
    colmatch = list()
    for col in cols_we_care:
        for i, colall in enumerate(colnames):
            if col == colall:
                colmatch.append(i)
    pp = paired_path.iloc[:,colmatch]
    pp["pid"] = paired_path["pid"]
    # normal blood / normal tumor / tumor primary / tumor recurrent
    # new columns for tumor, normal
    pp["tumor"] = np.nan
    pp["normal"] = np.nan
    for i in range(pp.shape[0]):
        ifna = pd.isnull(pp.iloc[i,])
        if (not ifna["NB"]):
            pp["normal"][i] = pp.iloc[i, 0]
        elif (not ifna["NT"]):
            pp["normal"][i] = pp.iloc[i, 1]
        else:
            print("no normal sample found!")
        if (not ifna["TP"]):
            pp["tumor"][i] = pp.iloc[i, 2]
        elif (not ifna["TR"]):
            pp["tumor"][i] = pp.iloc[i, 3]
        else:
            print("no tumor sample identfied!")
    pp2 = pp[["tumor", "normal", "pid"]]
    # split the columns for cohort, tss and participant
    pp2_ids = pp2.reset_index()["pid"].str.extract(r"([A-Z]+)-(..)-(....)$")
    pp2 = pd.concat([pp2_ids, pp2[["tumor","normal"]]], axis=1)
    pp2.columns = ["cohort","tss","pid","tumor","normal"]
    return(pp2)

            
    


# examples:
if __name__ == "__main__":
    ws_list = dalmatian.firecloud.api.list_workspaces().json()
    paired_path = get_pairs_from_wsname(re_match_wsname(ws_list))
    paired_path.to_csv("tcga_allpaired.csv")
    pp2 = match_pair(paired_path)
    pp2.to_csv("matched_paires_with_tss.csv")


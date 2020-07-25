from .. import igv_remote as ir
import numpy as np
import pandas as pd
# generate localhost http format
def format_url(uuid):
    return("http://localhost:5000/" + uuid + ".bam")


# read atsv containing the locations
df = pd.read_csv("sv-demo.tsv", sep = "\t")
df = df.sort_values(['case_id','seqnames', 'start'])

# only look at the ones that do not match
df = df[df.if_match == 0]

# set up igv_remote
ir.connect()
ir.set_saveopts(img_dir = "igv_snapshots", img_basename = "sv.png" ) # must be set!
ir.set_viewopts(view_type = "collapsed", viewaspairs = False, sort = "base") # optional
prev_tumor = ""
print(df)

print("type [next] to enter new view \n")
for index, view in df.iterrows():
    # print(view)
    action = input() 
    if action == "next" :# will only trigger downstream 
        print("start pos: chr{}:{}, strand={}".format(view['seqnames'], view['start'], view['strand']))
        print("end pos: chr{}:{}, strand={}".format(view['altchr'], view['altpos'], view['altstrand']))
        print("site1 annot={}, site2 annot={}".format(view['site1'], view['site2']))
        
        print(view["case_id"]) 
        
        
        
        if view['tumor'] != prev_tumor:
            ir.send("new")
            ir.load(format_url(view['tumor']), format_url(view['normal']))
            ir.goto_multiple(expand=300, chr1=view['seqnames'], pos1=view['start'], chr2=view['altchr'], pos2=view['altpos'])
            
        else: 
            print("Skipping bam reload ...")
            ir.goto_multiple(expand=300, chr1=view['seqnames'], pos1=view['start'], chr2=view['altchr'], pos2=view['altpos'])
            
        print("------------------ command sent -----------------")

        prev_tumor = view['tumor']
    else:
        print("Type [next] for next view")

print("Finished all views")

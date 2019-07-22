# igv_remote

An attempt to automate snapshot/navigate pipeline from ipython.

## Usage

The basic usage should be something like - 

```python
import igv_remote

# initialize a socket 
igv_remote.connect()

# setting some params for save and view options
igv_remote.set_saveopts(img_fulldir = "/home/qing/igv_snapshots/", img_basename = "test.png" ) # must be set!
igv_remote.set_viewopts(collapse = False, squish = True, viewaspairs = True ) # optional

# to get snapshot for a single location
igv_remote.load_single(gspath, # gspath for a single path
                       <misc position params>) # see details below

# to get snapshot for paired location
igv_remote.load_pair(tumor_path, normal_path,# paired paths, tumor in the upper track
                     <misc position params>) 
# close the socket
igv_remote.close()
```

The `<misc position params>` can be specified as chromosome and start and end positions, e.g. `chromosome=12, start_pos=345729,end_pos=345789 ` and each of the input could be a list, e.g. `chromosome=12, start_pos=[345729, 345758, 345799], end_pos=[347000, 347090, 347200]`  In case of list input for locations, we will take multiple screen shots for each location, resulting in multiple images named as `<imagename_x.png>.`

There are also misc utilities including

```python
# generate list of tuples [(chr, start, end)] for input to igv_remote.goto
igv_remote.parse_loc(chromosome, start, end)
# send navigate command to server
igv_remote.goto(*(chr, start, end))
```

A sample script can be found as `run.py` in this repo - **you need to adjust `imgfullpath` that works for you**. A sample data frame can be found at `test_df.csv` where it contains some gspaths of interest.

## Helpers

There are some helper function to parse firecloud workspace data from Dalmatian to your desired format in **dalmatian_helper.py**. `get_pairs_from_ws` and `match_pair` allows you to match tumor-normal pair for each sample_id, producing a dataframe with columns for `cohort` `tss` `pid` `tumor` and `normal`.

```python
import dalmatian
ws_list = dalmatian.firecloud.api.list_workspaces().json()
match_pair(get_pairs_from_wsname(re_match_wsname(ws_list)))
```

Please note that current implementation only works the format of "controlledAccess" data.

**locate_view.py** is another helper function that helps to match your callset to your interested genes and cohort.

```python
find_view(<callset pd dataframe>, 
          <dataframe from match_pair>,
          <interested gene>,
          <TCGA cohort>) #optional
```

The result will be a list of dictionary with `cohort`, `pid`,`gene` and `position`.

## Troubleshooting

* if something like `(Errno 111] Connection refused`  try to check if your IGV session is live or not.
* in case of `[Errno 32] *Broken pipe*` try to restart IGV
* `imgfullpath ` must be **full absolute path**, something like "/home/hurrialice/snapshots" and you need to make sure it exists!
* try run batch job directly on IGV for debug could be helpful
# igv_remote

An attempt to automate snapshot pipeline from ipython.

## Usage

The basic usage should be something like - 

```python
import igv_remote
# initialize a socket
igv_remote.connect()

# to get snapshot for a single location
igv_remote.load_single(gspath, # gspath for a single path
                       <misc position params>, # see below
                       imgfullpath, imgname, # where to save
                       collapse, squish, viewaspairs) # representation params (default=F,T,F)

# to get snapshot for paired location
igv_remote.load_pair(tumor_path, normal_path,# paired paths, tumor in the upper track
                     <misc position params>, 
                     imgfullpath, imgname, 
                     collapse, squish, viewaspairs) 
# close the socket
igv_remote.close()
```

The `<misc position params>` can be specified as chromosome and start and end positions, e.g. `chromosome=12, start_pos=345729,end_pos=345789 ` and each of the input could be a list, e.g. `chromosome=12, start_pos=[345729, 345758, 345799], end_pos=[347000, 347090, 347200]`  In case of list input for locations, we will take multiple screen shots for each location, resulting in multiple images named as `<imagename_x.png>.`

There are also misc utilities including

```python
# generate list of tuples [(chr, start, end)] for input to igv_remote.goto
igv_remote.parse_loc(chromosome, start, end)
# send navigate command to server
igv_remote.goto(socket, *(chr, start, end))
```

A sample script can be found as `run.py` in this repo - **you need to adjust `imgfullpath` that works for you**. A sample data frame can be found at `test_df.csv` where it contains some gspaths of interest.

## TODO

Add a helper function to generate dataframe of interest like `testdf`.

## Troubleshooting

* if something like `(Errno 111] Connection refused`  try to check if your IGV session is live or not.
* in case of `[Errno 32] *Broken pipe*` try to restart IGV
* `imgfullpath ` must be **full path**, something like "/home/hurrialice/snapshots" and you need to make sure it exists!
* try run batch job directly on IGV for debug could be helpful
# igv_remote

## Usage

The basic usage should be something like - 

```python
import igv_remote
# initialize a socket
sock = igv_remote.init()

# to get snapshot for a single location
igv_remote.load_single(sock, # socket
                       gspath, # gspath for a single path
                       <misc position params>, # see below
                       imgfullpath, imgname, # where to save
                       collapse, squish) # representation params (default=F,T)

# to get snapshot for paired location
igv_remote.load_single(sock, 
                       tumor_path, normal_path,# paired paths, tumor in the upper track
                       <misc position params>, 
                       imgfullpath, imgname, 
                       collapse, squish) 
# close the socket
igv_remote.close(sock)
```

The `<misc position params>` can be either specified as chromosome and start and end positions, e.g. `chromosome=12, start_pos=345729,end_pos=345789 `, or by gene symbol `genesymbol="TP53"`

A sample script can be found as `run.py` in this repo - just call `python3 run.py` . A sample dataframe can be found at `test_df.csv` where it contains some gspaths of interest.

## TODO

Add a helper function to generate dataframe of interest like `testdf`.

## Troubleshooting

* if something like `(Errno 111] Connection refused`  try to check if your IGV session is live or not.
* in case of `[Errno 32] *Broken pipe*` try to restart IGV
* `imgfullpath ` must be **full path**, something like "/home/hurrialice/snapshots" and you need to make sure it exists!
* try run batch job directly on IGV for debug could be helpful
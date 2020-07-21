
# igv_remote

Interacting with IGV desktop over a port with IGV batch commands in Python.

## Pre-requisite

A running IGV with proper authorization

## Usage

The most fundamental method is `send`, which accepts a string as described in [igv-commands](https://software.broadinstitute.org/software/igv/PortCommands). 

```
import igv_remote as ir
ir.connect()
ir.send("genome hg19")  # any port commands
ir.close()
```

However we also provided some wrappers for better UI, such as `load`, `goto` etc. Here is a fuller example:

```
import igv_remote as ir


# init socket
ir.connect()


# set view params
ir.set_saveopts(img_dir = "igv_snapshots/", img_basename = "test.png" ) # must be set!
ir.set_viewopts(collapse = False, squish = True, viewaspairs = True, sort = "base" ) # optional, this view options will be passed to all view panels

# load views / snapshot
ir.load(<tumor_bam>, <normal_bam>, ...)
ir.goto(<chr>, <pos>)
ir.snapshot()

# close socket
ir.close()
```

Similar structure can be found at`examples/run.py`, please log in with Google account and change the BAM paths to your authorized ones. For more complex port commands that are not implemented, please use `ir.send(<your port command>)` or make a PR!


## FAQ

- How to interact with DRS url?
  - As far as we know, IGV does not stream DRS url. However if a DRS url contains UUID, you can use UUID to generate a signed url (`http://...`) which IGV can acept. Detailed instructions are in [igv-gdc-buddy](https://github.com/getzlab/igv_gdc_buddy). `examples/batch_igv.py` is an example utilizing such interaction.

## Links

- [igv port commands](https://software.broadinstitute.org/software/igv/PortCommands)
- [igv batch script](https://software.broadinstitute.org/software/igv/batch)



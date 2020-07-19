
# igv_remote

Sending commands to IGV desktop over a port

## Usage

```
import igv_remote as ir


# init socket
ir.connect()


# set view params
ir.set_saveopts(img_dir = "igv_snapshots/", img_basename = "test.png" ) # must be set!
ir.set_viewopts(collapse = False, squish = True, viewaspairs = True, sort = "base" ) # optional

# load views / snapshot
ir.load(<tumor_bam>, <normal_bam>, ...)
ir.goto(<chr>, <pos>)
ir.snapshot()

# close socket
ir.close()
```

An example can be found at `run.py`, please log in with Google account and change the BAM paths to your authorized ones.

## FAQ

- How to interact with DRS url?
* As far as we know, IGV does not stream DRS url. However if a DRS url contains UUID, you can use UUID to generate a signed url (`http://...`) which IGV can acept. Detailed instructions are in [igv-gdc-buddy](https://github.com/getzlab/igv_gdc_buddy).

## Links

[igv port commands](https://software.broadinstitute.org/software/igv/PortCommands)
[igv batch script](https://software.broadinstitute.org/software/igv/batch)



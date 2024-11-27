# marine-user-guide
- Repository to store documents and resources used to create the Marine User Guide.

- See current version of the [Marine User Guide](https://github.com/glamod/marine-user-guide/blob/latex/mug_document_src/main.pdf)

## contents


### plotting environment
* documentation for environment set up and plotting routines: https://marine-user-guide.readthedocs.io/

* environment set up
```
./setenv.sh
./setpaths.sh
./init_version/
./env/
```

* scripts to generate plots
```
./common/
./data_summaries/
./data_summaries_sd/
./figures/
./figures_sd/
```

* config files for data summaries and plotting
```
./config/config/
```

* resources for the Marine User Guide document
  - ``` ./mug_document_src/ ```
  - Tex files under ./mug_document_src and ./mug_document_src/sections folders.
  - One sentence per line
  - compile with lualatex

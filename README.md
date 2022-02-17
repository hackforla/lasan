# Visualize LA 311 data 

Need a simple verion of results from [access the data workshop](https://github.com/researchsherpa/access-the-data-workshop-311-analysis) for Bulky Items (and LA Sanitation Dept in general).

I built this to be compact so it could run in binder.

## Contents

- Data directory contains two files:
   1) parquet file with geodata for all requests (note - it is a thinned version of columns)
   2) a clean version of Neighborhood Council polygons


- Notebooks directory contains two notebooks with multiple visualizations of the requests
   - bulky-items-choropleth.ipynb is a detailed workflow for bulky items
   - explore,ipynb is a parameterized version (with minimal narrative) to apply the workflow to different request types


- Notebooks can be explored with binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/researchsherpa/lasan/main?urlpath=lab)


## Setting Up Local Env

I use jupyter lab with ipywidgets and folium. The recipe is:

  1. Assuming anaconda is installed, repo cloned, and you're in the directory, environment.yml can be used to build a baseline lab env with conda:  `conda env create -f environment.yml`
  
  2. Activate the new env: `conda activate lasan`
 
  3. Fire up lab via `jupyter lab`
  
  4. Explore
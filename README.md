### Python Analysis Wrapper
This is a lightweight tool I built for organizing experiment output in python (e.g. data analysis & general machine learning work). Particularly useful for work on a remote server to avoid log/local/ipython notebooks.

This will make a timestamped and named directory for all your figures and redirect stdout log output to a file.

Example:
```
import numpy as np
from analysis_wrapper import AnalysisContext as Experiment
import matplotlib.pyplot as plt

with Experiment("plot_respect") as ex:
    # Log output will get saved even if your stuff crashes
    print("Doing some work")
    fig = plt.figure()
    # Do some plotting
    ex.save_fig(fig, "My Figure")
```

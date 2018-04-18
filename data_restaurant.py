import pandas as pd
import numpy as np



data = pd.read_excel("./data/map.xlsx")
print (np.array(data))
i = 0
for row in np.array(data) :
    for item in row :
        if item is not np.nan :
            x = item.split(", ")
            try : x = [float(t) for t in x ]
            except : pass
            print (x)
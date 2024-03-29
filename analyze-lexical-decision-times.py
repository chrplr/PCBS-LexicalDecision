""" Quick and dirty analysis of a data file generated by run-lexical-decision.py """

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols

if len(sys.argv) < 2:
    print(""" Usage: analyze-lexical-decision-times FILE

    Argument:
       FILE     : an .xpd file generated in `data` subfolder
    """)
    sys.exit()

data = pd.read_csv(sys.argv[1], comment='#')

data = data.loc[data.category != 'PSEUDO']  # exclude pseudowords

# detailed plot
sns.catplot(x='category', y='rt', hue='frequency', data=data)
plt.show()

# effects of frequency (hi vs. lo) and  category (noun vs verb)
sns.catplot(x="frequency",
            y='rt',
            col="category",
            data=data,
            kind="bar",
            height=2.5,
            aspect=.8)
plt.show()

# TODO: save the plots in graphics files

# Anova on Log Reaction Times with Frequency and Category as predictors
data['logrt'] = np.log10(data['rt'])
print(data.groupby(['cyapf<ategory', 'frequency']).describe())

anova_logrt = ols('logrt ~ frequency * category', data=data).fit()
table = sm.stats.anova_lm(anova_logrt)
print(table)

# TODO: save the formatted anova table in a file

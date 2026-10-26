"""Create legible report figures from the saved simulation output."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / 'outputs/simulated/cleaned.csv')
if set(d.data_origin) != {'SIMULATED'}:
    raise ValueError('Review the report labels before using a different data source.')
OUT = ROOT / 'report/work'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                     'axes.spines.top':False,'axes.spines.right':False,
                     'axes.labelsize':10,'xtick.labelsize':9,'ytick.labelsize':9})

def save(fig, name):
    fig.text(.99,.012,f'SIMULATED DATA  |  n = {len(d)}',ha='right',fontsize=8,color='#555555')
    fig.subplots_adjust(left=.13,right=.98,top=.97,bottom=.23)
    fig.savefig(OUT / name,dpi=250,facecolor='white')
    plt.close(fig)

fig, ax = plt.subplots(figsize=(6.2,3.1))
limit = max(700, np.ceil(d[['estimated_daily_minutes','recorded_daily_minutes']].to_numpy().max()/100)*100)
ax.scatter(d.estimated_daily_minutes,d.recorded_daily_minutes,s=19,color='#245c82',alpha=.7)
ax.plot([0,limit],[0,limit],'--',color='#a4492b',lw=1.2,label='Equal estimate and record')
ax.set(xlim=(-10,limit),ylim=(0,limit),xlabel='Estimated daily screen time (minutes)',ylabel='Recorded daily\naverage (minutes)')
ax.grid(alpha=.16);ax.set_axisbelow(True);ax.legend(loc='upper left',fontsize=8.5,frameon=False)
save(fig,'report_scatter.png')

fig, ax = plt.subplots(figsize=(6.2,2.45))
ax.hist(d.signed_error_minutes,bins=np.linspace(-250,250,11),color='#245c82',edgecolor='white')
ax.axvline(0,color='#a4492b',ls='--',lw=1.2,label='Zero error')
ax.axvline(d.signed_error_minutes.mean(),color='#363636',lw=1.2,label=f'Mean error {d.signed_error_minutes.mean():+.2f}')
ax.set(xlabel='Recorded minus estimated (minutes per day)',ylabel='Number of\nsimulated records')
ax.grid(axis='y',alpha=.16);ax.set_axisbelow(True);ax.legend(fontsize=8.5,frameon=False,loc='upper left')
save(fig,'report_errors.png')

fig, ax = plt.subplots(figsize=(6.2,2.3))
((quantiles,ordered),(slope,intercept,_)) = stats.probplot(d.signed_error_minutes,dist='norm')
ax.scatter(quantiles,ordered,s=15,color='#245c82',alpha=.75)
ax.plot(quantiles,intercept+slope*quantiles,color='#a4492b',lw=1.2)
ax.set(xlabel='Theoretical normal quantile',ylabel='Signed error\n(minutes per day)')
ax.grid(alpha=.16);ax.set_axisbelow(True)
save(fig,'report_qq.png')

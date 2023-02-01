#!/usr/bin/python3

import graphFunctions as c
import readCSVData as d
from matplotlib import pyplot as plt

fig, axs = plt.subplots(1,4, figsize=(15,7))
fig.subplots_adjust(wspace=0.5)


data = d.read_csv_data('csvs')
c.tuition_over_time(axs[3], data, [100654])
c.graduation_rate(axs[2], data, [100654])
c.admitance_rate(axs, data, [100654])
#c.cost_breakdown(axs[2], data, [100654])

school_list= [100654,100663,100690,100706,100724]
#c.compare_costs(data, school_list)
#c.acceptance_rates(data, school_list)
#c.compare_population(data, school_list)
#c.gender_outcomes_ratio(data, school_list)



#ax1 = c.fallback_xkcd(fig, ax1)
#ax2 = c.fallback_xkcd_2(fig, ax2)

for i in range(3):
	plt.setp(axs[i].get_xticklabels(),rotation=30, ha='right')
plt.title(d.get_name_from_id(data, [100654]))

plt.show()

#!/bin/user/python3

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import ConnectionPatch

# graph functions
# much of this is coppied or refrencing example code provided here:
# https://matplotlib.org/stable/gallery

# indivigual school graphs

# @return {int} return 1 if no data for graph
def tuition_over_time(ax, data, collage_id):
	data = get_data_on_collage(data, collage_id)
	tuition = list()
	tuition.append(data['DRVIC2021.Tuition and fees, 2018-19'].loc[data.index[0]])
	if tuition[0] == None:
		return 1
	tuition.append(data['DRVIC2021.Tuition and fees, 2019-20'].loc[data.index[0]])
	tuition.append(data['DRVIC2021.Tuition and fees, 2020-21'].loc[data.index[0]])
	tuition.append(data['DRVIC2021.Tuition and fees, 2021-22'].loc[data.index[0]])
	year = ['18/19','19/20','20/21','21/22']

	ax.plot(year, tuition, linewidth=2.0)
	ax.set_xlabel('School Year')
	ax.set_ylabel('Average Tuition')
	ax.set_title(label="Tuition Change Over Time")

	return 0


# TODO: This
# maybe not needed
def tuition_breakdown(data, collage_id):
	pass
	data = get_data_on_collage(data, collage_id)
	room_and_board = data['IC2021.Combined charge for room and board'].loc[data.index[0]]
	

# TODO Improve this
def graduation_rate(ax,data, collage_id):
	data = get_data_on_collage(data, collage_id)
	grad_rate = data['DRVGR2021.Graduation rate, total cohort'].loc[data.index[0]] # TODO: ckeck both columns for data
	if grad_rate == None:
		return 1
	trans_rate = data['DRVGR2021.Transfer-out rate, total cohort'].loc[data.index[0]]
	dropped = 100-grad_rate-trans_rate
	ax.pie([grad_rate, trans_rate, dropped], labels=["Graduated", "Transfered", "Dropped Out"],  
		wedgeprops={"linewidth":1,"edgecolor":'white'}, frame=True, autopct='%1.1f%%')
	ax.axis('off')
	ax.set_title(label="Student Outcomes")

	return 0

# TODO lines don't alighn properly
# NOTE: ax is list of 2 axises, not single axis like most others
def admitance_rate(ax, data, collage_id):
	data = get_data_on_collage(data, collage_id)
	# pie data
	admit_rate = data['DRVADM2021.Percent admitted - total'].loc[data.index[0]]
	if admit_rate == None:
		return 1
	reject_rate = 100 - admit_rate

	# get grad data data
	grad_rate = data['DRVGR2021.Graduation rate, total cohort'].loc[data.index[0]]
	trans_rate = data['DRVGR2021.Transfer-out rate, total cohort'].loc[data.index[0]]
	failure_rate = 100-grad_rate-trans_rate

	print(admit_rate)

	if grad_rate == None:
		# if admitans data but no score data
		#fig, ax = plt.subplot()
		ax.pie([admit_rate, reject_rate], labels=["% Admitted", "% Rejected"], radius=3, center=(4,4),
			wedgeprops={"linewidth":1,"edgecolor":white}, frame=True)
		ax.axis('equal')
		#fig.tex(0.5, 0.05, "Admitance Rate", ha='center')
		ax.set_title(label="Admitance Rate")
		return 0
		#plt.show()
		
	else:
		# draw fancier graph
		# set pie params
		ratios = [admit_rate/100, reject_rate/100]
		labels = ["% Admitted", "% Rejected"]
		explode = [0.1, 0]
		angle = -180 * ratios[0]

		# define pie chart
		wedges, *_ = ax[0].pie(ratios, autopct='%1.1f%%', startangle=angle,labels=labels, explode=explode)

		# set bar params
		outcome_ratios = [grad_rate/100, trans_rate/100, reject_rate/100]
		outcome_labels = ["% Graduate", "% Transfer", "% Dropout"]
		bottom = 1
		width = 0.2

		# set bar data
		for j, (height, label) in enumerate(reversed([*zip(outcome_ratios, outcome_labels)])):
			bottom -= height
			bc = ax[1].bar(0, height, width, bottom=bottom, color='C0',label=label, alpha=0.1+0.25*j)
			ax[1].bar_label(bc, labels=[f"{height:.0%}"], label_type='center')
		ax[1].set_title('Student Outcomes')
		ax[1].legend()
		ax[1].axis('off')
		ax[1].set_xlim(-2.5 * width, 2.5 * width)

		# graph title
		ax[0].set_title(label="Admitance Rate and Outcomes")

		# draw lines between graphs with connectionPatch
		theta1, theta2 = wedges[0].theta1, wedges[0].theta2
		center, r = wedges[0].center, wedges[0].r
		bar_height = sum(outcome_ratios)

		# draw top line
		x = r * np.cos(np.pi / 180 * theta2) + center[0]
		y = r * np.sin(np.pi / 180 * theta2) + center[1]
		con = ConnectionPatch(xyA=(-width/2, bar_height), coordsA=ax[1].transData, xyB=(x,y), coordsB=ax[0].transData)
		con.set_color([0,0,0])
		con.set_linewidth(2)
		ax[1].add_artist(con)

		# draw bottom line
		x = r * np.cos(np.pi / 180 * theta1) + center[0]
		y = r * np.sin(np.pi / 180 * theta1) + center[1]
		con = ConnectionPatch(xyA=(-width/2, 0), coordsA=ax[1].transData, xyB=(x,y), coordsB=ax[0].transData)
		con.set_color([0,0,0])
		con.set_linewidth(2)
		ax[1].add_artist(con)

		return 0
	return 1

def cost_breakdown(ax, data, collage_id):
	data = get_data_on_collage(data, collage_id)
	data.fillna(0)
	tuition = data['DRVIC2021.Tuition and fees, 2021-22'].loc[data.index[0]]
	if tuition == 0:
		return 1
	in_state_on_camp = data['DRVIC2021.Total price for in-state students living on campus 2021-22'].loc[data.index[0]]
	in_state_off_camp = data['DRVIC2021.Total price for in-state students living off campus (not with family)  2021-22'].loc[data.index[0]]
	out_state_on_camp = data['DRVIC2021.Total price for in-state students living on campus 2021-22'].loc[data.index[0]]
	out_state_off_camp = data['DRVIC2021.Total price for out-of-state students living off campus (not with family)  2021-22'].loc[data.index[0]]

	state_diff = out_state_on_camp - in_state_on_camp
	room_board = in_state_on_camp - tuition

	labels = ["Out of State\nOn Campus", "Out of State\nOff Campus", "In State\nOn Camput", "In State\nOff Campus"]
	tuition_list = [tuition, tuition, tuition, tuition]
	room_cost_list = [room_board, 0, room_board, 0]
	state_fees_list = [state_diff, state_diff, 0, 0]
	width = 0.35

	ax.bar(labels, tuition_list, width, label='Tuition')
	ax.bar(labels, state_fees_list, width, bottom=tuition, label="Out-Of-State Cost")
	ax.bar(labels, room_cost_list, width, bottom=state_fees_list, label="Dormatory Cost")

	ax.set_ylabel('Cost ($)')
	ax.set_title("Cost Breakdown")
	ax.legend()

	return 0


def granduation_breakdown(ax, data, school_id):
	pass
	#TODO: This


#--------------------------------------------------------------------------------------------------------
# School Groupd Figs

def compare_costs(ax, data, school_id_list):
	data = get_data_on_collage(data, school_id_list)
	data.fillna(0)
	school_list = data['institution name'].tolist()
	tuition_cost_in_state = data['IC2021_AY.In-state average tuition for full-time undergraduates'].tolist()
	tuition_cost_out_of_state = data['IC2021_AY.Out-of-state average tuition for full-time undergraduates'].tolist()

	# error checking, if all bars would be empty return 1
	reject_flag = 1
	for i in range(len(school_list)):
		if (tuition_cost_in_state[i] == 0) and (tuition_cost_out_of_state == 0):
			continue
		reject_flag = 0
	if reject_flag == 1:
		return 1

	# add newline characters to split school names
	for i in range(len(school_list)):
		tmp = school_list[i].split(' ')
		num = len(tmp)
		mid = int(num/2)
		tmp.insert(mid, '\n')
		school_list[i] = ' '.join(tmp)


	x=np.arange(len(school_list))
	width = 0.35

	#fig, ax = plt.subplots()
	in_state = ax.bar(x-width/2,tuition_cost_in_state, width, label="In State")
	out_state = ax.bar(x+width/2, tuition_cost_out_of_state, width, label="Out-Of-State")

	ax.set_ylabel("Cost ($)")
	ax.set_title('Tuition Cost by School')
	ax.set_xticks(x, school_list)
	ax.legend()

	ax.bar_label(in_state, padding=3)
	ax.bar_label(out_state, padding=3)

	return 0


def acceptance_rates(ax, data, school_id_list):
	data = get_data_on_collage(data, school_id_list)
	data.fillna(0)
	school_list = data['institution name'].tolist()
	accept_rate = data['DRVADM2021.Percent admitted - total'].tolist()
	
	# error checking, if all bars would be empty return 1
	reject_flag = 1
	for i in range(len(school_list)):
		if (accept_rate[i] == 0):
			continue
		reject_flag = 0
	if reject_flag == 1:
		return 1

	# add newline characters to split school names
	for i in range(len(school_list)):
		tmp = school_list[i].split(' ')
		num = len(tmp)
		mid = int(num/2)
		tmp.insert(mid, '\n')
		school_list[i] = ' '.join(tmp)

	x=np.arange(len(school_list))
	width = 0.35

	ax.bar(school_list, accept_rate, width=width)

	ax.bar_label(accept_rate, padding=3)
	ax.set_ylabel("% Accepted")
	ax.set_title("Acceptance Rate")
	ax.set_xticks(x, school_list)

	return 0



def compare_population(ax, data, school_id_list):
	data = get_data_on_collage(data, school_id_list)
	data.fillna(0)
	school_list = data['institution name'].tolist()
	headcount = data['DRVEF122021.Graduate 12-month unduplicated headcount'].tolist()

	# error checking, if all bars would be empty return 1
	reject_flag = 1
	for i in range(len(school_list)):
		if (headcount[i] == 0):
			continue
		reject_flag = 0
	if reject_flag == 1:
		return 1

	# add newline characters to split school names
	for i in range(len(school_list)):
		tmp = school_list[i].split(' ')
		num = len(tmp)
		mid = int(num/2)
		tmp.insert(mid, '\n')
		school_list[i] = ' '.join(tmp)

	x=np.arange(len(school_list))
	width = 0.35

	ax.bar(school_list, headcount, width=width)

	#ax.bar_label(headcount, padding=3)

	ax.set_ylabel("Number of Students")
	ax.set_title("Student Headcount")
	ax.set_xticks(x, school_list)

	return 0


def gender_outcomes_ratio(ax, data, school_id_list):
	data = get_data_on_collage(data, school_id_list)
	data.fillna(0)
	school_list = data['institution name'].tolist()
	grad_rate = data['DRVGR2021.Graduation rate, total cohort'].tolist()
	male_grad_rate = data['DRVGR2021.Graduation rate, men'].tolist()
	female_grad_rate = data['DRVGR2021.Graduation rate, women'].tolist()

	# error checking, if all bars would be empty return 1
	reject_flag = 1
	for i in range(len(school_list)):
		if (grad_rate[i] == 0):
			continue
		reject_flag = 0
	if reject_flag == 1:
		return 1

	# add newline characters to split school names
	for i in range(len(school_list)):
		tmp = school_list[i].split(' ')
		num = len(tmp)
		mid = int(num/2)
		tmp.insert(mid, '\n')
		school_list[i] = ' '.join(tmp)

	# transform data for stacke bar chart
	for i in range(len(school_list)):
		tmp_total = male_grad_rate[i] + female_grad_rate[i]
		male_grad_rate[i] = male_grad_rate[i] / tmp_total * grad_rate[i]
		female_grad_rate[i] = female_grad_rate[i] / tmp_total * grad_rate[i]

	x=np.arange(len(school_list))
	width = 0.35

	ax.bar(school_list, male_grad_rate, width, label="% Men")
	ax.bar(school_list, female_grad_rate, width, bottom=male_grad_rate, label="% Women")
	#TODO label bars
	#ax.bar_label(grad_rate, padding=3)

	ax.set_ylabel("Graduation Rate (%)")
	ax.set_title("Graduation Rate With Gender Breakdown")
	ax.set_xticks(x, school_list)
	plt.setp(ax.get_xticklabels(),rotation=30, ha='right')
	ax.legend()

	return 0



#--------------------------------------------------------------------------------------------------------
# NOTE: Only show this graph if nothing else can be displayed
# Joke Graph
def fallback_xkcd(fig, ax):
	with plt.xkcd():
		# Based on various graphs from XKCD by Randall Munroe

		#ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
		ax.spines.right.set_color('none')
		ax.spines.top.set_color('none')
		ax.set_yticks([])
		ax.set_ylim([-30, 10])

		data = np.ones(100)
		data[70:] -= np.arange(30)

		ax.annotate(
		    'WHEN A USER\nSEES THIS GRAPH', 
		    xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))
		ax.plot(data)

		ax.set_xlabel('time')
		ax.set_ylabel('user expectations')

	return 0

def fallback_xkcd_2(fig, ax):
	with plt.xkcd():
		#ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
		ax.bar([0, 1], [0, 100], 0.25)
		ax.spines.right.set_color('none')
		ax.spines.top.set_color('none')
		ax.xaxis.set_ticks_position('bottom')
		ax.set_xticks([0, 1])
		ax.set_xticklabels(['FOR THIS\nQUERY', 'IN OUR\nPROJECT'])
		ax.set_xlim([-0.5, 1.5])
		ax.set_yticks([])
		ax.set_ylim([0, 110])

		ax.set_title("Number of Graphs")

	return 0
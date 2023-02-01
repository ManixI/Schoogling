

class PageStats:
	def __init__(file):
		text_arr = list()
		with open(file, 'r') as fp:
			for line in file:
				text_arr.append(line)

		tmp = text_att[0].split('-')
		self.name = tmp[0]

		tmp = text_arr[1].split()
		self.sat_range = [tmp[3], tmp[5]]
		self.act_range = [tmp[11], tmp[13]]

		tmp = text_arr[2].split()
		self.dedline = tmp[18] + ' ' + tmp [19]
		self.acceptance_rate = tmp[27]

		tmp = text_arr[5].split()
		

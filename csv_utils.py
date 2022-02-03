import os
import System_Path

########################################################################
class Cell_Location(list):
	""""""
	#----------------------------------------------------------------------
	def __init__(self,row=-1,column=-1):
		"""Constructor"""
		super(Cell_Location,self).__init__([row,column])
	#----------------------------------------------------------------------
	def set_location(self,row,column):
		""""""
		self.row    = row
		self.column = column
	#----------------------------------------------------------------------
	@property
	def isValid(self):
		""""""
		return self[0] != -1 and self[1] != -1
	#----------------------------------------------------------------------
	def _get_row(self):
		""""""
		return self[0]
		
	#----------------------------------------------------------------------
	def _set_row(self,val):
		""""""
		if not isinstance(val,int):
			raise ValueError("Row Value Must Be Of Type int")
		self[0] = val
	#----------------------------------------------------------------------
	def _get_column(self):
		""""""
		return self[1]
		
	#----------------------------------------------------------------------
	def _set_column(self,val):
		""""""
		if not isinstance(val,int):
			raise ValueError("Column Value Must Be Of Type int")
		self[1] = val
	row    = property(_get_row,_set_row)
	column = property(_get_column,_set_column)
	
	
#----------------------------------------------------------------------
def convert_empty_indies_to_None(csv_rows):
	for row,rv in enumerate(csv_rows):
		for column,cv in enumerate([index.strip() for index in rv]):
			if cv == "":
				csv_rows[row][column] = None
			else:
				csv_rows[row][column] = cv
	return csv_rows

#----------------------------------------------------------------------
def convert_string_assinments_to_boolen_assinments(assinment_lists):
	res = []
	for i,assinment_list in enumerate(assinment_lists):
		assinments = []
		for j,assinment_item in enumerate(assinment_list):
			if assinment_item == "O":
				assinments.append(1)
			else:
				assinments.append(0)
		res.append(assinments)
	return res

#----------------------------------------------------------------------
def extract_rows(csv,start,end):
	res = []
	for row in range(start,end+1):
		item = csv[row]
		res.append(item)
	return res

#----------------------------------------------------------------------
def extract_columns_from_row(csv,row,start,end):
	res = []
	for column in range(start,end):
		item = csv[row][column]
		res.append(item)
	return res

#----------------------------------------------------------------------
def extract_column_index_from_rows(csv,start,end,index):
	res = []
	for row in range(start,end):
		item = csv[row][index]
		res.append(item)
	return res

#----------------------------------------------------------------------
def find_first_None_value(csv,row_start,column_start):
	row_end = len(csv)
	cell = Cell_Location()
	for r in range(row_start,row_end):
		column_end = len(csv[r])
		
		for c in range( column_start, column_end ):
			
			if csv[r][c] == None:
				cell.set_location(r,c)
				break
		if cell.isValid:
			break
			
	return cell

#----------------------------------------------------------------------
def find_first_valid_data(csv,row_start,column_start):
	row_end = len(csv)
	cell = Cell_Location()
	for r in range(row_start,row_end):
		column_end = len(csv[r])
		for c in range( column_start, column_end ):
			
			if not csv[r][c] == None:
				cell.set_location(r,c)
				break
		if cell.isValid:
			break
	return cell

#----------------------------------------------------------------------
def remove_invalid_rows(csv):
	res = []
	for data_range in find_valid_data_row_ranges(csv):
		res.append(csv[data_range[0]])
	return res

#----------------------------------------------------------------------
def remove_empty_tail_columns_from_rows(csv):
	for row,rv in enumerate(csv):
		for column,cv in enumerate([str(index).strip().replace("None","") for index in rv]):
			if len(cv):
				last_valid_Column_index = column
		if not len(rv)-1 <= last_valid_Column_index:
			del csv[row][last_valid_Column_index+1:]
	return csv

#----------------------------------------------------------------------
def create_nomlized_grid_cells(csv):
	larget_row_lenght = find_largest_row_lenght(csv)
	res = []
	for row,rv in enumerate(csv):
		temp_list = []
		if len(rv) >= larget_row_lenght:
			temp_list = rv[:larget_row_lenght+1]
		elif len(rv) < larget_row_lenght:
			temp_list = rv
			while len(temp_list) < larget_row_lenght:
				temp_list.append(None)
		res.append(temp_list)
	return res

#----------------------------------------------------------------------
def remove_invalid_columns(csv):
	master_column_num = find_largest_column_lenght(csv)
	master_row_num    = find_last_valid_row(csv)
	for column in range(master_column_num+1):
		remove_check = True
		for row,rv in enumerate(csv):
			try:
				cell_value = rv[column]
				if not cell_value == None:
					remove_check = False
					break
			except IndexError:
				break
		if remove_check:
			for row in range(master_row_num+1):
				if len(csv[row])-1 >= column:
					del csv[row][column]
	return csv

#----------------------------------------------------------------------
def find_valid_data_row_ranges(csv):
	ranges = []
	current_row = 0
	current_column = 0
	range_start = [-1,-1]
	range_end   = [-1,-1]
	
	while current_row < len(csv):
		if range_start[0] == -1 and range_start[1] == -1:
			
			while current_column < len(csv[current_row]):
				
				if not csv[current_row][current_column] ==  None:
					range_start = [current_row,current_column]
					break
				else:
					current_column += 1
					
		if range_end[0] == -1 and range_end[1] == -1 and range_start[0] != -1 and range_start[1] != -1:
			
			while current_column < len(csv[current_row]):
				
				if csv[current_row][current_column] ==  None and csv[current_row][0] ==  None:
					range_end = [current_row,current_column]
					ranges.append(range_start+range_end)
					range_start = [-1,-1]
					range_end   = [-1,-1]
					
					break
				current_column += 1
				
			if range_start[0] != -1 and range_start[1] != -1:
				range_end = [current_row,current_column]
				ranges.append(range_start+range_end)
				range_start = [-1,-1]
				range_end   = [-1,-1]
				
		current_row += 1
		current_column = 0
	return ranges

#----------------------------------------------------------------------
def extract_column_indices_from_rows(csv,row_start,row_end,column_start,column_end):
	res = []
	for row in range(row_start,row_end):
		column_items = []
		for column in range(column_start,column_end):
			item = csv[row][column]
			column_items.append(item)
		res.append(column_items)
	return res
#----------------------------------------------------------------------
def find_largest_column_lenght(csv):
	largest_lenght = 0
	for r in csv:
		for i in reversed(list(range(len(r)))):
			if not r[i]=="":
				if i > largest_lenght:
					largest_lenght = i
	return largest_lenght

#----------------------------------------------------------------------
def find_largest_row_lenght(csv):
	largest_lenght = 0
	for r in csv:
		for index,row in enumerate(r):
			if row != None:
				if index > largest_lenght:
					largest_lenght = index
	return largest_lenght

##----------------------------------------------------------------------
def get_Last_Valid_row_for_column(csv,column):
	last_valid_index  = 0
	for row,rv in enumerate(csv):
		try:
			cell_value = rv[column]
			if not cell_value == None:
				last_valid_index = row
		except IndexError:
			pass
	return last_valid_index
#----------------------------------------------------------------------
def find_last_valid_row(csv):
	largest_lenght = 0
	for i in reversed(list(range(len(csv)))):
		r = csv[i]
		if not "".join([str(item) for item in r]) == "":
			if i > largest_lenght:
				largest_lenght = i
	return largest_lenght
#----------------------------------------------------------------------
def load_file(filePath):
	with file(filePath,"r") as data:
		lines = data.readlines()
		data.close()
		csv = []
		for row in lines:
			row_items = [str(item.strip()) for item in row.split(",")]
			csv.append(row_items)
		optimized = optimized_csv(csv)
		return optimized

#----------------------------------------------------------------------
def load_String(val):
	lines = val.splitlines()
	csv = []
	for row in lines:
		row_items = [str(item.strip()) for item in row.split(",")]
		csv.append(row_items)
	optimized = optimized_csv(csv)
	return optimized


#----------------------------------------------------------------------
def optimized_csv(csv):
	optimized = convert_empty_indies_to_None(csv)
	optimized = remove_invalid_rows(optimized)
	optimized = remove_invalid_columns(optimized)
	optimized = create_nomlized_grid_cells(optimized)
	return optimized

#----------------------------------------------------------------------
def find_CSV_Header_Value(csv, tag):
	cell = Cell_Location()
	for col, value in enumerate(csv[0]):
		if value == tag:
			cell.set_location(0,col)
			break
	return cell
#----------------------------------------------------------------------
def find_CSV_Sub_Header_Value(csv, tag):
	cell = Cell_Location()
	for col, value in enumerate(csv[1]):
		if value == tag:
			cell.set_location(0, col)
			break
	return cell

#----------------------------------------------------------------------
def find_CSV_Tag(csv, tag):
	cell = Cell_Location()
	for r, row in enumerate(csv):
		for c, col in enumerate(row):
			if col == tag:
				cell.set_location(r,c)
				break
		if cell.isValid:
			break
	return cell



########################################################################
class CSV_Grid(list):
	#----------------------------------------------------------------------
	def __init__(self,*args,**kwargs):
		super(CSV_Grid,self).__init__(args)
		self._subgrids = {}
		file_path = kwargs.get("file")
		lines     = kwargs.get("lines")
		if isinstance(file_path,(str,System_Path.Path)):
			file_path = System_Path.Path(file_path)
			if file_path.exists():
				self.load_file(file_path)
		if not lines is None:
			self.load_string(lines)
		
	#----------------------------------------------------------------------
	def get_Last_Valid_row_for_column(self,column):
		return get_Last_Valid_row_for_column(self, column)
	#----------------------------------------------------------------------
	def iterRows(self):
		"""iterate Through Each Row Of The CSV_Grid"""
		for row in self:
			yield row	
	#----------------------------------------------------------------------
	def iterColumns(self):
		"""iterate Through Each Column Of The CSV_Grid"""
		current_column = 0
		for row in self:
			yield row
			
	#----------------------------------------------------------------------
	def find_Header_Name(self, tag):
		return find_CSV_Header_Value(self, tag)
	#----------------------------------------------------------------------
	def find_Sub_Header_Name(self, tag):
		return find_CSV_Sub_Header_Value(self, tag)
	#----------------------------------------------------------------------
	def find_tag(self, tag):
		return find_CSV_Tag(self, tag)
	#----------------------------------------------------------------------
	@property
	def row_len(self):
		return len(self)
	#----------------------------------------------------------------------
	def save_file(self,filePath,remove_tails=True):
		"""Output CSV_Grid Back A CSV File"""
		lines = []
		if remove_tails:
			csv=remove_empty_tail_columns_from_rows(self)
		else:
			csv=self
		for row in csv:
			line = []
			for column in row:
				if column == None:
					line.append("")
				else:
					line.append("%s" % str(column) )
			line = ",".join(line)+"\n"
			lines.append(line)
		with file(filePath,"w") as data:
			isinstance(data,file)
			data.writelines(lines)
		
	#----------------------------------------------------------------------
	def load_file(self, filePath):
		csv = load_file(filePath)
		for row in csv:
			self.append(row)
	#----------------------------------------------------------------------
	def load_string(self, lines):
		csv = load_String(lines)
		for row in csv:
			self.append(row)

	#----------------------------------------------------------------------
	def extract_rows(self, start, end):
		""""""
		return extract_rows(self, start, end)
		
	#----------------------------------------------------------------------
	def extract_columns_from_row(self, row, start, end):
		""""""
		return extract_columns_from_row(self, row, start, end)
	#----------------------------------------------------------------------
	def create_Sub_Grid(self,name,row_start, row_end, column_start, column_end):
		""""""
		subgrid = Sub_Grid(name, self, row_start, row_end, column_start, column_end)
		return subgrid
	#----------------------------------------------------------------------
	def has_Sub_Grid(self,name):
		""""""
		return name in self._subgrids
	
	#----------------------------------------------------------------------
	def iter_Sub_Grids(self,sort_by_name=True):
		""""""
		grid_names = list(self._subgrids.keys())
		if sort_by_name:
			grid_names.sort()
			
		for grid_name in grid_names:
			yield self._subgrids[grid_name]
	#----------------------------------------------------------------------
	def update_subGrids(self):
		""""""
		for name,grid in list(self._subgrids.items()):
			grid.update_subGrids()
		
	
	largest_column_lenght = property(find_largest_column_lenght)
	last_valid_row        = property(find_last_valid_row)
	valid_data_row_ranges = property(find_valid_data_row_ranges)

########################################################################
class Sub_Grid(CSV_Grid):
	""""""
	#----------------------------------------------------------------------
	def __init__(self,name,master_grid,row_start=-1,row_end=-1,column_start=-1,column_end=-1):
		"""Constructor"""
		if not isinstance(master_grid,CSV_Grid):
			raise ValueError("Master Grid Must Be A Subclass of CSV_Grid")
		
		super(Sub_Grid,self).__init__()
		self._name        = name
		self.master_grid  = master_grid
		self.master_grid._subgrids[name] = self
		self.row_start    = row_start
		self.row_end      = row_end
		self.column_start = column_start
		self.column_end   = column_end
		self.update()
		
	@property
	def name(self):
		"""I'm the 'x' property."""
		return self._name

	@name.setter
	def name(self, value):
		self.master_grid._subgrids[value]=self
		self.master_grid.remove(self._name)
		self._name = value

	#----------------------------------------------------------------------
	def update(self):
		""""""
		self.reset()
		if self.row_start != -1 and self.row_end != -1 and self.column_start != -1 and self.column_end != -1:
			for row in self.master_grid[self.row_start:self.row_end+1]:
				items = []
				for index in range(self.column_start,self.column_end+1):
					try:
						item = row[index]
						items.append(item)
					except IndexError:
						print("index error accored during updated")
				self.append(items)
				
	#----------------------------------------------------------------------
	def update_Master_Grid(self):
		""""""
		if self.row_start != -1 and self.row_end != -1 and self.column_start != -1 and self.column_end != -1:
			for row,rv in enumerate(self):
				for col,cv in enumerate(rv):
					current_value = self.master_grid[self.row_start+row][self.column_start+col]
					if not cv == current_value:
						self.master_grid[self.row_start+row][self.column_start+col] = cv
		if hasattr(self.master_grid,"update_Master_Grid"):
			self.master_grid.update_Master_Grid()
	#----------------------------------------------------------------------
	def reset(self):
		for index in range(len(self)):
			self[index] = None
		while(len(self)):
			del self[0]

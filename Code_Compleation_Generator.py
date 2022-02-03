
import xml.etree.ElementTree as etree

_Tag_To_Class = dict()
########################################################################
class Code_Element_Base(etree.Element):
	""""""
	#----------------------------------------------------------------------
	def __init__(self,parent, tag, attrib={}, **extra):
		"""Constructor"""
		super(Code_Element_Base,self).__init__(tag, attrib)
		self._parent = parent
		self._root_element = None
	#----------------------------------------------------------------------
	@property
	def parent_element(self):
		""""""
		return self._parent
	#----------------------------------------------------------------------
	@property
	def children(self):
		""""""
		return self._children
	#----------------------------------------------------------------------
	@property
	def root_element(self):
		""""""
		if self._root_element == None:
			elem = self
			while not elem._parent == None:
				elem = elem._parent
			self._root_element = elem
		return self._root_element

########################################################################
class Code_ui(Code_Element_Base):
	""""""
	#----------------------------------------------------------------------
	@property
	def widgets(self):
		''' '''
		return self.iterfind("widget")
	#----------------------------------------------------------------------
	@property
	def all_widgets(self):
		''' '''
		return self.iter(tag="widget")
	#----------------------------------------------------------------------
	@property
	def ui_Class(self):
		''' '''
		return self.find("class")
	#----------------------------------------------------------------------
	def generate_Code_Compleatshion(self,classBase="QWidget",modual_prefix="QT"):
		""""""
		code = []  
		code.append("########################################################################")
		code.append("class _CODE_COMPLEATION_HELPER(%s.%s):" % (modual_prefix,classBase))
		code.append('\t""""""')
		code.append("\t#----------------------------------------------------------------------")
		code.append("\tdef __init__(self,parent=None):")
		code.append("\t\t''''''")
		code.append("\t\tsuper(_CODE_COMPLEATION_HELPER,self).__init__(parent=parent)")
		code.append("\t\tif False:")
		
		for wig in self.all_widgets:
			if wig.class_name.startswith("Q"):
				code.append("\t\t\tself.%s = %s.%s()" % (wig.name,modual_prefix,wig.class_name))
			else:
				code.append("\t\t\tself.%s = %s()" % (wig.name,wig.class_name))
		res = "\n".join(code)
		return res

_Tag_To_Class["ui"] = Code_ui
########################################################################
class Code_class(Code_Element_Base):
	""""""
	#----------------------------------------------------------------------
	@property
	def name(self):
		""""""
		return self.text

_Tag_To_Class["class"] = Code_class

########################################################################
class Code_widget(Code_Element_Base):
	""""""
	#----------------------------------------------------------------------
	@property
	def name(self):
		""""""
		return self.get("name")
	#----------------------------------------------------------------------
	@property
	def class_name(self):
		""""""
		return self.get("class")
	@property
	#----------------------------------------------------------------------
	def child_Widgets(self):
		""""""
		return self.iterfind(tag="widget")

_Tag_To_Class["widget"] = Code_widget

#----------------------------------------------------------------------
def UI_Element_Factory(parent,tag, attrib={}, **extra):
	""""""
	if tag in list(_Tag_To_Class.keys()):
		cls = _Tag_To_Class[tag]
		return cls(parent, tag, attrib)
	else:
		return Code_Element_Base(parent,tag, attrib)
########################################################################
class UI_Tree_Builder(etree.TreeBuilder):
	""""""
	def __init__(self):
		super(UI_Tree_Builder,self).__init__(element_factory=UI_Element_Factory)

	def start(self, tag, attrs):
		self._flush()
		self._last = elem = self._factory(self._last,tag, attrs)
		if self._elem:
			self._elem[-1].append(elem)
		self._elem.append(elem)
		self._tail = 0
		return elem

#----------------------------------------------------------------------
def Xml_From_File(file_path):
	parser = etree.XMLParser(target=UI_Tree_Builder())
	tree = etree.parse(file_path,parser=parser)
	root = tree.getroot()
	return root

#----------------------------------------------------------------------
def Print_Code(file_path,classBase="QWidget",modual_prefix="QT"):
	data = Xml_From_File(file_path)
	print((data.generate_Code_Compleatshion(classBase,modual_prefix)))

if __name__ == "__main__":
	#Print_Code(r"u:\dloveridge\AW_Asset_Assembly_System\SOFTWARE_TOOLS\Maya\Maya_Assembly_State_System\UI\AW_States_Manager.ui",modual_prefix="PYQT")
	#Print_Code(r"u:\dloveridge\AW_Asset_Assembly_System\SOFTWARE_TOOLS\Maya\Maya_Assembly_State_System\UI\Sub_Widget_Create_Node.ui",modual_prefix="PYQT")
	# Print_Code(r"C:\Users\dloveridge\Documents\AW_Systems_Code\Software\Maya\Scripts\Tools\Selection_Set_Manager\UI\AW_Display_Layer_Editor.ui",modual_prefix="PYQT")
	Print_Code(r"\\isln-smb\utilitiesdev\Maya\Display_Layer_Compair\Display_Layer_Compair_Main_Window.ui",modual_prefix="PYQT")

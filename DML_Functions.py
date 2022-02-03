#----------------------------------------------------------------------
def flatten(x):
	result = []
	for el in x:
		if hasattr(el, "__iter__") and not isinstance(el, str):
			result.extend(flatten(el))
		else:
			result.append(el)
	return result


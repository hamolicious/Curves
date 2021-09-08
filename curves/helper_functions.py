
def clamp(value, max_value, min_value):
	value = min(value, max_value)
	value = max(value, min_value)

	return value



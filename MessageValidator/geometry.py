__author__ = 'Antonio Vaccarino'



def isPointInPolygon (point, polygon):

	Xo = point[0]
	Yo = point[1]

	for i in range (0, len(polygon)-1):

		segment = polygon[i-1], polygon[i]

		Xva = segment[0][0]
		Yva = 

# booklet -p 0-99 -s 5
# -p	Pages (default all)
# -s	Sheets per "page group" (find correct term) (default auto = as many as is required to fit all pages)

def iter_pages( pages ):
	for output_page in range( pages / 4 ):
		first = output_page * 2
		last = pages - 1 - first

		# Front
		yield first + 1
		yield last - 1

		# Back
		yield last
		yield first

def test_pagegroups():
	assert pagegroups( 1 ) == 1
	assert pagegroups( 2 ) == 1
	assert pagegroups( 3 ) == 1
	assert pagegroups( 4 ) == 1

	assert pagegroups( 5 ) == 2
	assert pagegroups( 6 ) == 2
	assert pagegroups( 7 ) == 2
	assert pagegroups( 8 ) == 2
	
	assert pagegroups( 16 ) == 4

def scale_matix( scale_x, scale_y = None ):
	if scale_y == None:
		scale_y = scale_x

	return [
		[ scale_x, 0,	    0 ],
		[ 0, 	   scale_y, 0 ],
		[ 0,	   0,	    1 ]
	]

def build_page():
	import PyPDF2.utils, math
	src = PyPDF2.PdfFileReader( file( 'test.pdf', 'rb' ) )
	out = PyPDF2.PdfFileWriter()

	size = src.getPage(0).mediaBox.upperRight
	aspect = size[0] / size[1]

	newpage = out.addBlankPage( *size )
	print newpage

	page1 = src.getPage( 0 )
		#page1.scaleBy( float( aspect ) )
	#page1.scaleBy( .1 )

	print page1.mediaBox.upperRight
	print size[0] * aspect, size[1] * aspect

	tx = size[ 0 ]
	ty = 0
	rotation = 90

	scale = scale_matix( aspect )
	translation = [[1, 0, 0],
					[0, 1, 0],
					[tx, ty, 1]]
	rotation = math.radians(rotation)
	rotating = [[math.cos(rotation), math.sin(rotation), 0],
	[-math.sin(rotation), math.cos(rotation), 0],
	[0, 0, 1]]
	rtranslation = [[1, 0, 0],
	[0, 1, 0],
	[tx, ty, 1]]
	ctm = PyPDF2.utils.matrixMultiply(scale, rotating)
	ctm = PyPDF2.utils.matrixMultiply(ctm, translation)
	#ctm = PyPDF2.utils.matrixMultiply(ctm, rtranslation)

	newpage.mergeTransformedPage( page1, [ ctm[0][0], ctm[0][1],
ctm[1][0], ctm[1][1],
ctm[2][0], ctm[2][1]] )

	out.write( file( 'out.pdf', 'wb' ) )


def test_pagesequence():
	pagesequence = iter_pages( 4 )
	assert pagesequence.next() == 1
	assert pagesequence.next() == 2
	assert pagesequence.next() == 3
	assert pagesequence.next() == 0

	pagesequence = iter_pages( 8 )
	assert pagesequence.next() == 1
	assert pagesequence.next() == 6
	assert pagesequence.next() == 7
	assert pagesequence.next() == 0
	assert pagesequence.next() == 3
	assert pagesequence.next() == 4
	assert pagesequence.next() == 5
	assert pagesequence.next() == 2

	pagesequence = iter_pages( 16 )
	assert pagesequence.next() == 1
	assert pagesequence.next() == 14
	assert pagesequence.next() == 15
	assert pagesequence.next() == 0
	assert pagesequence.next() == 3
	assert pagesequence.next() == 12
	assert pagesequence.next() == 13
	assert pagesequence.next() == 2
	assert pagesequence.next() == 5
	assert pagesequence.next() == 10
	assert pagesequence.next() == 11
	assert pagesequence.next() == 4
	assert pagesequence.next() == 7
	assert pagesequence.next() == 8
	assert pagesequence.next() == 9
	assert pagesequence.next() == 6

if __name__ == '__main__':
	#test_pagesequence()
	build_page()
#!/bin/env python2
# booklet -p 0-99 -s 5
# -p	Pages (default all)
# -s	Sheets per "page group" (find correct term) (default auto = as many as is required to fit all pages)

import math, PyPDF2.utils

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


def translation_matrix( x, y = None ):
	if y == None:
		y = x

	return [
		[ 1, 0, 0 ],
		[ 0, 1, 0 ],
		[ x, y, 1 ]
	]

def scale_matix( scale_x, scale_y = None ):
	if scale_y == None:
		scale_y = scale_x

	return [
		[ scale_x, 0,	    0 ],
		[ 0, 	   scale_y, 0 ],
		[ 0,	   0,	    1 ]
	]

def rotation_matrix( angle, rad = False ):
	if not rad:
		angle = math.radians( angle )

	return [
		[  math.cos( angle ), math.sin( angle ), 0 ],
		[ -math.sin( angle ), math.cos( angle ), 0 ],
		[  0,                 0,                 1 ]
	]

def merge_matrix( translation_matrix ):
	return [
		translation_matrix[0][0], translation_matrix[0][1],
		translation_matrix[1][0], translation_matrix[1][1],
		translation_matrix[2][0], translation_matrix[2][1]
	]

def build_page():
	src = PyPDF2.PdfFileReader( file( 'test.pdf', 'rb' ) )
	out = PyPDF2.PdfFileWriter()

	size = src.getPage(0).mediaBox.upperRight
	aspect = size[0] / size[1]

	newpage = out.addBlankPage( *size )

	page1 = src.getPage( 0 )

	tm = PyPDF2.utils.matrixMultiply( scale_matix( aspect ), rotation_matrix( -90 ) )
	tm = PyPDF2.utils.matrixMultiply( tm, translation_matrix( 0, size[ 1 ] / 2 ) )

	newpage.mergeTransformedPage( page1, merge_matrix( tm ) )

	page2 = src.getPage( 1 )

	tm = PyPDF2.utils.matrixMultiply( scale_matix( aspect ), rotation_matrix( -90 ) )
	tm = PyPDF2.utils.matrixMultiply( tm, translation_matrix( 0, size[ 1 ] ) )

	newpage.mergeTransformedPage( page2, merge_matrix( tm ) )

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
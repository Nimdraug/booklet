#!/bin/env python2
# booklet -p 0-99 -s 5
# -p    Pages (default all)
# -s    Sheets per "page group" (find correct term) (default auto = as many as is required to fit all pages)

import math, PyPDF2.utils

def iter_pages( pages ):
    if pages % 4:
        pages = pages + 4 - pages % 4

    for output_page in range( pages / 4 ):
        first = output_page * 2
        last = pages - 1 - first

        # Front
        yield first, -90, 1, .5
        yield last, -90, 1, 0

        # Back
        yield first + 1,  90, 0, 1
        yield last - 1,  90, 0, .5


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
        [ scale_x, 0,       0 ],
        [ 0,       scale_y, 0 ],
        [ 0,       0,       1 ]
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
    
    outpage = out.addBlankPage( *size )

    for i, v in enumerate( iter_pages( src.numPages ) ):
        p, r, x, y = v
        if p < src.numPages:
            srcpage = src.getPage( p )

            tm = PyPDF2.utils.matrixMultiply( scale_matix( aspect ), rotation_matrix( -r ) )
            tm = PyPDF2.utils.matrixMultiply( tm, translation_matrix( float( size[0] ) * x, float( size[1] ) * y ) )

            outpage.mergeTransformedPage( srcpage, merge_matrix( tm ) )

        if i < src.numPages and i % 2:
            outpage = out.addBlankPage( *size )

    out.write( file( 'out.pdf', 'wb' ) )

def test_pagesequence():
    pagesequence = iter_pages( 4 )
    assert pagesequence.next() == ( 0, -90, 1, .5 )
    assert pagesequence.next() == ( 3, -90, 1, 0 )
    assert pagesequence.next() == ( 1,  90, 0, 1 )
    assert pagesequence.next() == ( 2,  90, 0, .5 )

    pagesequence = iter_pages( 6 )
    assert pagesequence.next() == ( 0, -90, 1, .5 )
    assert pagesequence.next() == ( 7, -90, 1, 0 )
    assert pagesequence.next() == ( 1,  90, 0, 1 )
    assert pagesequence.next() == ( 6,  90, 0, .5 )
    assert pagesequence.next() == ( 2, -90, 1, .5 )
    assert pagesequence.next() == ( 5, -90, 1, 0 )
    assert pagesequence.next() == ( 3,  90, 0, 1 )
    assert pagesequence.next() == ( 4,  90, 0, .5 )

    pagesequence = iter_pages( 12 )
    assert pagesequence.next() == ( 0, -90, 1, .5 )
    assert pagesequence.next() == ( 11, -90, 1, 0 )
    assert pagesequence.next() == ( 1,  90, 0, 1 )
    assert pagesequence.next() == ( 10,  90, 0, .5 )
    assert pagesequence.next() == ( 2, -90, 1, .5 )
    assert pagesequence.next() == ( 9, -90, 1, 0 )
    assert pagesequence.next() == ( 3,  90, 0, 1 )
    assert pagesequence.next() == ( 8,  90, 0, .5 )
    assert pagesequence.next() == ( 4, -90, 1, .5 )
    assert pagesequence.next() == ( 7, -90, 1, 0 )
    assert pagesequence.next() == ( 5,  90, 0, 1 )
    assert pagesequence.next() == ( 6,  90, 0, .5 )

    pagesequence = iter_pages( 16 )
    assert pagesequence.next() == ( 0, -90, 1, .5 )
    assert pagesequence.next() == ( 15, -90, 1, 0 )
    assert pagesequence.next() == ( 1,  90, 0, 1 )
    assert pagesequence.next() == ( 14,  90, 0, .5 )
    assert pagesequence.next() == ( 2, -90, 1, .5 )
    assert pagesequence.next() == ( 13, -90, 1, 0 )
    assert pagesequence.next() == ( 3,  90, 0, 1 )
    assert pagesequence.next() == ( 12,  90, 0, .5 )
    assert pagesequence.next() == ( 4, -90, 1, .5 )
    assert pagesequence.next() == ( 11, -90, 1, 0 )
    assert pagesequence.next() == ( 5,  90, 0, 1 )
    assert pagesequence.next() == ( 10,  90, 0, .5 )
    assert pagesequence.next() == ( 6, -90, 1, .5 )
    assert pagesequence.next() == ( 9, -90, 1, 0 )
    assert pagesequence.next() == ( 7,  90, 0, 1 )
    assert pagesequence.next() == ( 8,  90, 0, .5 )

if __name__ == '__main__':
    #test_pagesequence()
    build_page()
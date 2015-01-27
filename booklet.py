# booklet -p 0-99 -s 5
# -p	Pages (default all)
# -s	Sheets per "page group" (find correct term) (default auto = as many as is required to fit all pages)

def iter_pages( pages ):
	for output_page in range( pages / 4 ):
		first = output_page * 2
		yield first
		yield first + 1

		last = pages - 1 - first
		yield last - 1
		yield last


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


def test_pagesequence():
	pagesequence = iter_pages( 4 )
	assert pagesequence.next() == 0
	assert pagesequence.next() == 1
	assert pagesequence.next() == 2
	assert pagesequence.next() == 3

	pagesequence = iter_pages( 8 )
	assert pagesequence.next() == 0
	assert pagesequence.next() == 1
	assert pagesequence.next() == 6
	assert pagesequence.next() == 7
	assert pagesequence.next() == 2
	assert pagesequence.next() == 3
	assert pagesequence.next() == 4
	assert pagesequence.next() == 5

	pagesequence = iter_pages( 16 )
	assert pagesequence.next() == 0
	assert pagesequence.next() == 1
	assert pagesequence.next() == 14
	assert pagesequence.next() == 15
	assert pagesequence.next() == 2
	assert pagesequence.next() == 3
	assert pagesequence.next() == 12
	assert pagesequence.next() == 13
	assert pagesequence.next() == 4
	assert pagesequence.next() == 5
	assert pagesequence.next() == 10
	assert pagesequence.next() == 11
	assert pagesequence.next() == 6
	assert pagesequence.next() == 7
	assert pagesequence.next() == 8
	assert pagesequence.next() == 9

if __name__ == '__main__':
	test_pagesequence()
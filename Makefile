# Project: Kaye
# Makefile created by Peter Schultz

DIR_backups=backups/
DIR_images=images/
DIR_releases=releases/
DIR_schema=schema/
DIR_source=source/

PROJECT=Kaye

clean:
	temps=`find . -iname \*.pyc`
	rm $(temps)

distclean: clean
	




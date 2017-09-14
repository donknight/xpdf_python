import os
import sys

# should cover windows, linux, or mac distros using either the pdftotext distro or the XPDF tools distro
if any(i in os.environ['PATH'] for i in ('pdftotext', 'XPDF')):
	pass
else:
	sys.exit("Did not detect correctly installed xpdf. Please follow install instructions at: https://github.com/ecatkins/xpdf_python.")

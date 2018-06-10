" --------------------------------
" Add our plugin to the path
" --------------------------------
python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------
function! s:TestUtil(...) abort
python3 << endOfPython

import vim
import vimbufferutil

#abc = vimbufferutil.AddBufferContent()
#
#abc.removeandwait(1)
#abc.addandwait("hello from line2", 2)
#abc.removeandwait(3)
#
#abc.conduct(vim.current.buffer)

endOfPython
endfunction


function! s:RecordAllFunctions(...) abort
python3 << endOfPython

import vim
import countparentheses
import vimbufferutil
import autodoc
import time
from shutil import copyfile

vim.current.buffer.append("import autodocparameters", 0)
vim.current.buffer.append("from autodocparameters import recordparametertype", 0)

path = vim.eval("s:path")
flag_return_type = (vim.eval("g:autodoc_display_return_type") == "1")

copyfile("{}/parameters.py".format(path), "./autodocparameters.py")


for row, line in enumerate(vim.current.buffer):
	extra = line.lstrip()
	if extra.startswith("def ") and (row==0 or not vim.current.buffer[row-1].lstrip().startswith("@")):
		space = " " * (len(line) - len(extra))
		vim.current.buffer.append("", row)
		vim.current.buffer[row] = space + "@recordparametertype"


vim.command("w")
otherfile = ""
if int(vim.eval("a:0")) == 0:
	vim.current.buffer[-1] = "autodocparameters.logfunctionparameters()"
	vim.command("!python %")
elif vim.eval("a:1").startswith("python"):
	otherfile = vim.eval("a:2")
	if otherfile != vim.eval("expand('%')"):
		with open(otherfile, 'a+') as f:
			f.write(vim.eval("expand('%:t:r')") + ".autodocparameters.logfunctionparameters()"+'\n')
		vim.command("!" + " ".join(vim.eval("a:000")))
	else:
		otherfile = ""
		vim.current.buffer[-1] = "autodocparameters.logfunctionparameters()"
		vim.command("!" + " ".join(vim.eval("a:000")))
elif vim.eval("a:1").endswith(".py"):
	otherfile = vim.eval("a:1")
	print(otherfile)
	print(vim.eval("expand('%')"))
	if otherfile != vim.eval("expand('%')"):
		with open(otherfile, 'a+') as f:
			f.write(vim.eval("expand('%:t:r')") + ".autodocparameters.logfunctionparameters()"+'\n')
		vim.command("!python " + " ".join(vim.eval("a:000")))
	else:
		otherfile = ""
		vim.current.buffer[-1] = "autodocparameters.logfunctionparameters()"
		vim.command("!python " + " ".join(vim.eval("a:000")))
else:
	vim.current.buffer[-1] = "autodocparameters.logfunctionparameters()"
	vim.command("!python % " + " ".join(vim.eval("a:000")))

vim.command("g/import autodocparameters/d")
vim.command("g/from autodocparameters import recordparametertype/d")
vim.command("g/@recordparametertype/d")
vim.command("g/autodocparameters.logfunctionparameters/d")

if vim.eval("g:autodoc_typehint_style") == "pep484":
	autodoc.addpep484hint(vim.current.buffer, flag_return_type)
else:
	autodoc.adddocstring_paramtype(vim.current.buffer, flag_return_type)
if vim.eval("g:autodoc_display_runtime_info") == "1":
	autodoc.adddocstring_runtime_info(vim.current.buffer)

if otherfile != "":
	readFile = open(otherfile)
	lines = readFile.readlines()
	readFile.close()
	w = open(otherfile,'w')
	w.writelines([item for item in lines[:-1]])
	w.close()

vim.command("w")
vim.command('call delete("autodocparameters.py")')
vim.command('call delete(".autodocparameters.log")')

endOfPython
endfunction


function! s:RecordCurrentFunction(...) abort
python3 << endOfPython

import vim
import countparentheses
import autodoc

currentindent = 999

for row in range(vim.current.window.cursor[0]-1, -1, -1):
	line = vim.current.buffer[row]
	extra = line.lstrip()
	if len(extra) == 0:
		continue
	elif (len(line) - len(extra)) // 4 >= currentindent:
		continue
	elif extra.startswith("def ") and (row==0 or not vim.current.buffer[row-1].lstrip().startswith("@")):
		space = " " * (len(line) - len(extra))
		vim.current.buffer.append("", row)
		vim.current.buffer[row] = space + "@recordparametertype"
		break
	else:
		currentindent = (len(line) - len(extra)) // 4


vim.current.buffer.append("import autodocparameters", 0)
vim.current.buffer.append("from autodocparameters import recordparametertype", 0)

path = vim.eval("s:path")
flag_return_type = (vim.eval("g:autodoc_display_return_type") == "1")

vim.command("!cp {}/parameters.py ./autodocparameters.py".format(path))

vim.command("w")
otherfile = ""
if int(vim.eval("a:0")) == 0:
	vim.current.buffer[-1] = "autodocparameters.logfunctionparameters()"
	vim.command("!python %")
elif vim.eval("a:1").startswith("python"):
	otherfile = vim.eval("a:2")
	if otherfile != vim.eval("expand('%')"):
		with open(otherfile, 'a+') as f:
			f.write(vim.eval("expand('%:t:r')") + ".autodocparameters.logfunctionparameters()"+'\n')
		vim.command("!" + " ".join(vim.eval("a:000")))
	else:
		otherfile = ""
		vim.current.buffer[-1] = "autodocparameters.logfunctionparameters()"
		vim.command("!" + " ".join(vim.eval("a:000")))
elif vim.eval("a:1").endswith(".py"):
	otherfile = vim.eval("a:1")
	print(otherfile)
	print(vim.eval("expand('%')"))
	if otherfile != vim.eval("expand('%')"):
		with open(otherfile, 'a+') as f:
			f.write(vim.eval("expand('%:t:r')") + ".autodocparameters.logfunctionparameters()"+'\n')
		vim.command("!python " + " ".join(vim.eval("a:000")))
	else:
		otherfile = ""
		vim.current.buffer[-1] = "autodocparameters.logfunctionparameters()"
		vim.command("!python " + " ".join(vim.eval("a:000")))
else:
	vim.current.buffer[-1] = "autodocparameters.logfunctionparameters()"
	vim.command("!python % " + " ".join(vim.eval("a:000")))

vim.command("g/import autodocparameters/d")
vim.command("g/from autodocparameters import recordparametertype/d")
vim.command("g/@recordparametertype/d")
vim.command("g/autodocparameters.logfunctionparameters/d")

if vim.eval("g:autodoc_typehint_style") == "pep484":
	autodoc.addpep484hint(vim.current.buffer, flag_return_type)
else:
	autodoc.adddocstring_paramtype(vim.current.buffer, flag_return_type)
if vim.eval("g:autodoc_display_runtime_info") == "1":
	autodoc.adddocstring_runtime_info(vim.current.buffer)

if otherfile != "":
	readFile = open(otherfile)
	lines = readFile.readlines()
	readFile.close()
	w = open(otherfile,'w')
	w.writelines([item for item in lines[:-1]])
	w.close()


vim.command("w")
vim.command('call delete("autodocparameters.py")')
vim.command('call delete(".autodocparameters.log")')

endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------

let s:path = expand('<sfile>:p:h')

if !exists("g:autodoc_display_return_type")
	let g:autodoc_display_return_type = 1
endif

if !exists("g:autodoc_display_runtime_info")
	let g:autodoc_display_runtime_info = 0
endif

if !exists("g:autodoc_typehint_style")
	let g:autodoc_typehint_style = "pep484"
endif

command! -nargs=* RecordParameter :call s:RecordAllFunctions(<f-args>)
command! -nargs=* RecordCurrentFunction :call s:RecordCurrentFunction(<f-args>)
command! -nargs=* TestUtil :call s:TestUtil(<f-args>)

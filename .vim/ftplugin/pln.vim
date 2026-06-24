" commands to change checkboxes
command! ToDo :s/\v^\s*-\s*\[[ Mx\?\~]\]/- [ ]/
command! Done :s/\v^\s*-\s*\[[ Mx\?\~]\]/- [x]/
command! Move :s/\v^\s*-\s*\[[ Mx\?\~]\]/- [M]/
command! Maybe :s/\v^\s*-\s*\[[ Mx\?\~]\]/- [?]/
command! WontDo :s/\v^\s*-\s*\[[ Mx\?\~]\]/- [\~]/

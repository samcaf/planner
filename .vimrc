let g:planner_root = fnamemodify(resolve(expand("<sfile>:p")), ":h")

" .vimrc for custom planner files (~/.vimrc needs execr to find this)
autocmd BufRead,BufNewFile *.pln setfiletype pln

" re-build: create new html associated with the current file when saved
autocmd BufWritePost *.pln !bash bin/build.sh

" allowing local .vim
set runtimepath^=./.vim
set runtimepath+=./.vim/after

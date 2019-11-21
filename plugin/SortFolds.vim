" SortFolds.vim - Sort closed folds based on first line
" Maintainer:   Oliver Breitwieser
" Version:      0.2.0
" License:      MIT license

if exists("g:loaded_sort_folds")
    finish
endif
let g:loaded_sort_folds = 1

let s:save_cpo = &cpo
set cpo&vim

if !has("python3")
    echohl WarningMsg
    echom "SortFolds requires +python."
    finish
endif

vnoremap <silent> <Plug>SortFolds :call SortFolds#SortFolds()<CR>

if !hasmapto("<Plug>SortFolds", "v")
    vmap <leader>sf <Plug>SortFolds
endif

let &cpo = s:save_cpo

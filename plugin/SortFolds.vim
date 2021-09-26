" SortFolds.vim - Sort closed folds based on first line
" Maintainer:   Oliver Breitwieser
" Version:      1.3.0
" License:      MIT license

if exists("g:loaded_sort_folds")
    finish
endif
let g:loaded_sort_folds = 1

let s:save_cpo = &cpo
set cpo&vim

if !has("python3")
    echohl WarningMsg
    echom "SortFolds requires +python3."
    finish
endif

if !exists("g:sort_folds_ignore_case")
  let g:sort_folds_ignore_case = 0
endif

vnoremap <silent> <Plug>SortFolds :call SortFolds#SortFolds()<CR>

if !hasmapto("<Plug>SortFolds", "v")
    vmap <leader>sf <Plug>SortFolds
endif

command! -range SortFolds <line1>,<line2>call SortFolds#SortFolds()

let &cpo = s:save_cpo

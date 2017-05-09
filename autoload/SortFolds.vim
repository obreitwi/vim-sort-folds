" SortFolds.vim - Sort closed folds based on first line
" Maintainer:   Oliver Breitwieser
" Version:      0.1.0
" License:      MIT license

py import vim
py import SortFolds

function! SortFolds#SortFolds() range
    silent execute a:firstline. "," . a:lastline . " py SortFolds.sort_folds()"
endfunction

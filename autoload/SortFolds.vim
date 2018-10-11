" SortFolds.vim - Sort closed folds based on first line
" Maintainer:   Oliver Breitwieser
" Version:      0.2.0
" License:      MIT license

py import vim
py import SortFolds

function! SortFolds#SortFolds(...) range
    let a:sortline = get(a:, 0, 0)
    silent execute a:firstline. "," . a:lastline .
                \ " py SortFolds.sort_folds(" . a:sortline .  ")"
endfunction

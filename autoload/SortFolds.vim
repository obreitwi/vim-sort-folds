" SortFolds.vim - Sort closed folds based on first line
" Maintainer:   Oliver Breitwieser
" Version:      1.3.0
" License:      MIT license

py3 import vim
py3 import sort_folds

function! SortFolds#SortFolds(...) range
    let sortline = get(a:, 0, 0)
    silent execute a:firstline. "," . a:lastline .
                \ " py3 sort_folds.sort_folds(" . sortline .  ")"
endfunction

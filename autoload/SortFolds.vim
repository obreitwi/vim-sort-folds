" SortFolds.vim - Sort closed folds based on first line
" Maintainer:   Oliver Breitwieser
" Version:      0.2.0
" License:      MIT license

py3 import vim
py3 import SortFolds

function! SortFolds#SortFolds(...) range
    let sortline = get(a:, 0, 0)
    silent execute a:firstline. "," . a:lastline .
                \ " py3 SortFolds.sort_folds(" . sortline .  ")"
endfunction

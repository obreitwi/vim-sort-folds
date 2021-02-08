# SortFolds

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/obreitwi/vim-sort-folds/Run%20tests%20in%20vim)](https://github.com/obreitwi/vim-sort-folds/actions?query=workflow%3A%22Run+tests+in+vim%22)

## Overview

![](https://raw.github.com/obreitwi/vim-sort-folds/master/doc/demo.gif)  
_(Demo \w [SimpylFold](https://github.com/tmhedberg/SimpylFold),
colorscheme [xoria256](https://github.com/vim-scripts/xoria256.vim))_

Sorting folds is not easily possible in vanilla vim. You could join all lines
in a fold, sort and split them up again; however, it is time consuming and
tedious.

This little plugin solves that issue: It sorts a visually selected region while
keeping closed folds intact. Since folds can be created in a variety of ways,
it is therefore straight-forward to sort arbitrary groups of text based on
their first line.

One use-case (demonstrated above and the original motivation for this plugin)
is to sort functions alphabetically after the fact.

Furthermore, it is possible to sort based on other lines than then first.


## Installation

`SortFolds` is compatible with most plugin managers for vim.
Just drop the following line in your `.vimrc`:

`Plugin 'obreitwi/vim-sort-folds'`
(for [Vundle](https://github.com/VundleVim/Vundle.vim))

`Plug 'obreitwi/vim-sort-folds'`
(for [vim-plug](https://github.com/junegunn/vim-plug))


## Mappings

Per default, sorting visually selected folds is mapped to `<leader>sf`, if
available, but can be easily remapped.


## Configuration

You can ignore case when sorting by modifying this variable:
```vim
let g:sort_folds_ignore_case = 1
```
Default is `0`


## Custom key-function

Sometimes you need to sort folds by some custom key.
For this reason, you can define a custom sort function in Python that maps fold
contents (essentially a list of lines) to a a key (a string) by which the fold
will be sorted.

Afterwards, you need to set `g:sort_folds_key_function` to the name of the
function.

### Example: Sort BibTeX-entries by key only, but not entry type

BibTeX-entries can be of several types (`article`, `book`, `inproceedings`,
`online`, to name a few…). However, we might want to sort them by citekey
regardless of type.

Hence, we might add a piece of code to extract the citekey:
```vim
py3 <<EOF
def get_citekey(fold):
    # very crude extraction without regexes
    return fold[0].split("{")[1].split(",")[0]

import sort_folds
sort_folds.register_key_function(get_citekey)
EOF

autocmd FileType bib let sort_folds_key_function="get_citekey"
```

Note: `get_citekey` is already part of the
[builtin functions](python3/sort_folds/key_functions.py).


## Python 3

`vim-sort-folds` is now Python 3 compatible. The last Python 2 compatible
commit is still available as tag
[`last-py2`](https://github.com/obreitwi/vim-sort-folds/releases/tag/last-py2).

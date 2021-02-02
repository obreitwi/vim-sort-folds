# SortFolds

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

## Python 3

`vim-sort-folds` is now Python 3 compatible. The last Python 2 compatible
commit is still available as tag
[`last-py2`](https://github.com/obreitwi/vim-sort-folds/releases/tag/last-py2).

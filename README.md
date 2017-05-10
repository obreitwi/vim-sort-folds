# SortFolds

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


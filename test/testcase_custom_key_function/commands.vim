:set foldmethod=marker
:py3 <<EOF
def my_key_function(fold):
    return int(fold[1].split(":")[1].strip())
import sort_folds
sort_folds.register_key_function(my_key_function)
EOF
:let g:sort_folds_key_function="my_key_function"
:%call SortFolds#SortFolds()
:messages
:wq

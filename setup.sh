DIR="$( cd "$( dirname $BASH_SOURCE )" && pwd )"
cd $DIR
alias pip="python ~/.local/bin/pip"
~/.local/bin/pip install -e . --user

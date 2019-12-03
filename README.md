# Install server:

## add user

root@Apollo:~#
    adduser peter
    usermod -a -G sudo peter

## install packages, venv and bot, then run

peter@Apollo:~/
    sudo apt install bash-completion virtualenv git
    
    # python3.6
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6

    mkdir -p work && cd work
    virtualenv -p /usr/bin/python3.6 venv
    cd venv
    git clone https://github.com/PeterErnsthaft/asdf.git
    . bin/activate
    pip install -r asdf/requirements.txt 
    mkdir saves
    echo "token einfügen nicht vergessen"
    python asdf/src/main.py token



# Install server:

## add user

root@Apollo:~#

    adduser peter
    usermod -a -G sudo peter

## install packages, venv and bot, then run

peter@Apollo:~/

    sudo apt install bash-completion virtualenv git locales
    
    # python3.6
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
    
    # proper locale settings
    echo "LC_ALL=en_US.UTF-8" | sudo tee -a /etc/environment
    echo "en_US.UTF-8 UTF-8" | sudo tee -a /etc/locale.gen
    echo "LANG=en_US.UTF-8" | sudo tee /etc/locale.conf
    sudo locale-gen en_US.UTF-8

    mkdir -p work && cd work
    virtualenv -p /usr/bin/python3.6 venv
    cd venv
    git clone https://github.com/PeterErnsthaft/asdf.git score_bot
    . bin/activate
    pip install -r score_bot/requirements.txt 
    mkdir saves
    echo "token einfügen nicht vergessen"
    python score_bot/src/main.py token
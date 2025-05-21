# Update packages
sudo apt update

# Install pyenv
curl -fsSL https://pyenv.run | bash

# Add pyenv to Fish configuration
echo 'set -x PYENV_ROOT $HOME/.pyenv' >> ~/.config/fish/config.fish
echo 'if test -d $PYENV_ROOT/bin' >> ~/.config/fish/config.fish
echo '    set -x PATH $PYENV_ROOT/bin $PATH' >> ~/.config/fish/config.fish
echo 'end' >> ~/.config/fish/config.fish
echo 'status --is-interactive; and pyenv init - fish | source' >> ~/.config/fish/config.fish

# Install dependencies
sudo apt update; sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl git libncursesw5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
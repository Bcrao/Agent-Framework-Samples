sudo apt update
sudo apt upgrade -y
sudo apt-get install git-lfs
conda activate base
pip uninstall agent-framework -y
pip uninstall agent-framework-azure-ai -y
git config fetch.showForcedUpdates true
pip install -r ./.devcontainer/requirements.txt --constraint ./.devcontainer/constraints.txt -U

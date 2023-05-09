function install
    set root (pwd)
    for dir in pyrrho app
        poetry env use 3.11
        echo "installing dependencies for $dir" && cd $dir && poetry lock --no-update && poetry install --sync
        cd $root
    end
    cd $root
end

#!/bin/sh
# Create links in .git/hooks to files in git-hooks

# Iterate over files
for hook in git-hooks/*; do
    # ascii file is a special one that we don't want to run
    basename=$(basename $hook)
    if [ $basename != "ascii" ]; then
        echo "Setting up git hook for $hook"
        chmod +x $hook
        ln -sf ../../${hook} .git/hooks/$basename
    fi
done

echo "Git hooks setup complete"

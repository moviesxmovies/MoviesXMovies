# Serve the Zensical site locally
runserver:
    uv run zensical serve

# Setup the development environment
setup:
    uv sync

# Create a new Zensical project
new:
    uv run zensical new .

# Clean the built site
clean:
    rm -rf site/

# Build the static site
build: clean
    uv run zensical build

# Deploy the static site (group = \d+, path = '/some/path')
deploy group server path:
    ssh {{ server }} "mkdir -p {{ path }}/g{{ group }}/"
    rsync -avz --delete ./site/ {{ server }}:{{ path }}/g{{ group }}/
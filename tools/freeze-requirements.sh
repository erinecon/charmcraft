#!/bin/bash -eux

requirements_fixups() {
  req_file="$1"

  # Python apt library pinned to source.
  sed -i '/^python-apt==/d' "$req_file"
}

venv_dir="$(mktemp -d)"

uv venv --python=3.10 "$venv_dir"
# shellcheck source=/dev/null
. "$venv_dir/bin/activate"

# Pull in host python3-apt site package to avoid installation.
site_pkgs="$(readlink -f "$venv_dir"/lib/python3.*/site-packages/)"
temp_dir="$(mktemp -d)"
pushd "$temp_dir"
apt download python3-apt
dpkg -x ./*.deb .
cp -r usr/lib/python3/dist-packages/* "$site_pkgs"
popd

uv pip install -e .
uv pip freeze --exclude-editable > requirements.txt
requirements_fixups "requirements.txt"

uv pip install -e .[dev]
uv pip freeze --exclude-editable > requirements-dev.txt
requirements_fixups "requirements-dev.txt"

rm -rf "$venv_dir"

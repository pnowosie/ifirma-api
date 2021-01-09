# Example invoice creation from yaml file

## Try this

1. Create a venv and activate
   `make venv && . ./.venv/bin/activate`

1. Inspect the requirements.txt file. You can also install directly from github repository, replace file's content with
`-e git+git@github.com:pnowosie/ifirma-api.git#egg=pnowosie.ifirma-api`

1. Install a package directly from pypi
   `make install`

1. Inspect the yaml file and provide your email address

1. Provide ifirma api access details via environment variables `
export IFIRMA_API_USERNAME=example@email.com` and `export IFIRMA_API_KEY=010203040A0B0C0D`

1. Create invoice
   `make invoice`

1. Clean
   `deactivate && make clean`
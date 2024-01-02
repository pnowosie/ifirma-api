# Example invoice creation (from yaml file) and other actions

You need to clone this repo or download [source release](https://github.com/pnowosie/ifirma-api/releases) to your local directory.

## Try this

I assume all actions will be invoke from this `examples` folder.

### 1. Install dependencies into venv
   `make install`

### 2. Provide ifirma api access details via environment variables `
export IFIRMA_API_USERNAME=example@email.com` and `export IFIRMA_API_KEY=010203040A0B0C0D`

Alternatively you can provide credentials to env.example file and rename it to `.env`


### 3. Inspect the yaml file and provide your email address

### 4. Create invoice
   `make <command>`

where command is:
- invoice
- list-invoices
- check-month (requires `abonent_API_KEY` is set)

### 5. Clear

Remove secrets and venv artifacts
`make clean clean-env`


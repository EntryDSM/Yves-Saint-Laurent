import os
import hvac

VAULT_URL = 'https://vault.entrydsm.hs.kr'
VAULT_SECRET_CONFIG_URL = 'service-secret/{env}/yves-saint-laurent'
VAULT_DB_URL = 'database/creds/yves-saint-laurent-{env}'


def create_vault_client():
    client = hvac.Client(url=VAULT_URL)

    if os.environ.get("VAULT_TOKEN"):
        client.token = os.environ["VAULT_TOKEN"]
    elif os.environ.get("GITHUB_TOKEN"):
        client.auth.github.login(token=os.environ.get("GITHUB_TOKEN"))

    return client


def db_credential_url(env):
    env = 'prod' if env == 'production' else 'test'
    return VAULT_DB_URL.format(env=env)


def vault_secret_url(env):
    env = 'prod' if env == 'production' else 'test'
    return VAULT_SECRET_CONFIG_URL.format(env=env)


def config(env):
    client = create_vault_client()

    database_credential = client.read(db_credential_url(env=env))['data']

    get_config = {
        'env': env,
        'DATABASE_USERNAME': database_credential.values(),
        'DATABASE_PASSWORD': database_credential.values()
    }

    return get_config

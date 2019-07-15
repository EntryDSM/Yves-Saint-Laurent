import os
import hvac

VAULT_URL = 'https://vault.entrydsm.hs.kr'
VAULT_SECRET_CONFIG_URL = 'service-secret/{env}/yves-saint-laurent'
VAULT_DB_URL = 'database/creds/yves-saint-laurent-{env}'


def create_vault_client():
    client = hvac.Client(url=VAULT_URL)

    try:
        if os.environ.get("VAULT_TOKEN"):
            client.token(os.environ.get("VAULT_TOKEN"))
        elif os.environ.get("GITHUB_TOKEN"):
            client.auth.github.login(token=os.environ.get("GITHUB_TOKEN"))
    except ValueError:
        print("No token")

    return client


def get_db_credential_url(env):
    env = 'prod' if env == 'production' else 'test'
    return VAULT_DB_URL.format(env=env)


def get_vault_secret_url(env):
    env = 'prod' if env == 'production' else 'test'
    return VAULT_SECRET_CONFIG_URL.format(env=env)


def get_config(env):
    client = create_vault_client()

    database_credential = client.read(get_db_credential_url(env=env))['data']

    config = {
        'env': env,
        'DATABASE_USERNAME': database_credential.get('username'),
        'DATABASE_PASSWORD': database_credential.get('password')
    }

    config.update(**client.read(get_vault_secret_url(env=env))['data'])

    return config

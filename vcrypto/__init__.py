from vcrypto.vcrypto import create_password
from vcrypto.vcrypto import export_secret
from vcrypto.vcrypto import get_secret
from vcrypto.vcrypto import init_vcrypto
from vcrypto.vcrypto import save_secret


# Alias `get_secret` as `read_secret`
read_secret = get_secret

# Explicitly define public API
__all__ = [
    "init_vcrypto",
    "get_secret",
    "read_secret",
    "save_secret",
    "create_password",
    "export_secret",
]

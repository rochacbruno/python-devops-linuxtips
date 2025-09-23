import re
import logging
import sys

# matches key=value or key:value or key = value or key : value
secret_pattern = re.compile(r'\b(senha|password|token|key)\s*[:=]\s*\S+', re.IGNORECASE)

# Configurar logging
class SecretFilter(logging.Filter):
    def filter(self, record):
        """Detect and omit sensitive information"""
        if secret_pattern.search(record.getMessage()):
            record.args = tuple("*****" for arg in record.args)
        return True

logger = logging.getLogger('secure_logger')
handler = logging.StreamHandler(sys.stdout)
handler.addFilter(SecretFilter())
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Uso do logger
secret_value = "senha123"
logger.info("Iniciando aplicação")
logger.debug("Conectando ao banco com senha=%s", secret_value)
logger.error("Erro ao autenticar usuário com senha: %s", secret_value)
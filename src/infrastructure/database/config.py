# src/infrastructure/database/config.py
from infrastructure.database.session import obter_bd

# Criamos um apelido (alias): quem chamar get_db vai usar a sua obter_bd nativamente
get_db = obter_bd
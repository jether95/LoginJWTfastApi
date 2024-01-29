from passlib.context import CryptContext

# Crea una instancia del objeto CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Utiliza la función hash de passlib para encriptar la contraseña
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Utiliza la función verify de passlib para verificar la contraseña
    return pwd_context.verify(plain_password, hashed_password)

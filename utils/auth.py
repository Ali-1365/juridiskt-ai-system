def check_password(username, password):
    """Enkel autentisering"""
    return username == "admin" and password == "hemligt"

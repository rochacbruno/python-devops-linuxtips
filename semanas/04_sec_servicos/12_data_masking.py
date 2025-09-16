def mask_email(email: str) -> str:
    """Mascara endereço de email"""
    if '@' not in email:
        return '***'
    local, domain = email.split('@')
    if len(local) <= 2:
        masked = '*' * len(local)
    else:
        masked = local[0] + '*' * (len(local)-2) + local[-1]
    return f"{masked}@{domain}"

def mask_cpf(cpf: str) -> str:
    """Mascara CPF mantendo apenas últimos 2 dígitos"""
    clean = ''.join(c for c in cpf if c.isdigit())
    return '*' * 9 + clean[-2:] if len(clean) >= 11 else '***'

print(f"Email: {mask_email('bruno@example.com')}")
print(f"CPF: {mask_cpf('123.456.789-00')}")
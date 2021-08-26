"""
Wyjątki podczas pracy automatu vendingowego (automat sprzedający napoję)
"""

class NotStrException(Exception):
    """
    Wyjątek jest zgłaszany po przekazaniu do set_text, zamiast text, typ nie jest str
    """
    pass


class TypeObjectException(Exception):
    """
    Wyjątek jest generowany podczas transmisji, zamiast obj nie jest kontrolką
    """
    pass


class NoGoodsForSelling(Exception):
    """
    Wyjątek jest generowany, gdy nie wybrano żadnego produktu, po kliknięciu przycisku Kup(Buy)
    """
    pass

class ProductIsNotAvailable(Exception):
    """
    Wyjątek jest generowany, gdy wybrany element jest niedostępny.
    """
    pass


class NoProductWithThisCode(Exception):
    """
    Wyjątek jest generowany, gdy zostanie wybrany kod spoza listy
    """
    pass


class InsufficientFunds(Exception):
    """
    Wyjątek jest generowany, gdy nie ma wystarczającej ilości pieniędzy na zakup produktu
    """
    pass
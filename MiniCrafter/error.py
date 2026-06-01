class MiniCrafterError(Exception):
    pass


class MiniSyntaxError(MiniCrafterError):
    def __init__(self, message):
        super().__init__(f"Yooooooooooo ur team leader here its Avi aapki grammer kamzor hogyi T_T sad {message}")


class MiniRuntimeError(MiniCrafterError):
    pass


class MiniLexicalError(MiniCrafterError):
    def __init__(self, message):

        super().__init__(
            f" Lexical Error broooo token nai ban pare kyaaaa \n"
        )
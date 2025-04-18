class TokenRepository:
    # Simple in-memory blacklist for tokens
    blacklisted_tokens = set()

    @staticmethod
    def blacklist_token(token):
        TokenRepository.blacklisted_tokens.add(token)

    @staticmethod
    def is_token_blacklisted(token):
        return token in TokenRepository.blacklisted_tokens

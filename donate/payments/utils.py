from functools import lru_cache

from django.utils.translation.trans_real import parse_accept_lang_header

from .constants import CURRENCIES, LOCALE_CURRENCY_MAP


def freeze_transaction_details_for_session(details):
    details = details.copy()
    details['amount'] = str(details['amount'])
    return details


@lru_cache(maxsize=1000)
def get_currency_info(currency):
    return CURRENCIES[currency].copy()


@lru_cache(maxsize=1000)
def get_default_currency(language_header):
    """
    Parse a HTTP Accept-Language header and return the best match for default
    currency for the user's preferred language.
    """
    for lang, p in parse_accept_lang_header(language_header):
        try:
            return LOCALE_CURRENCY_MAP[lang]
        except KeyError:
            # If the language has a region, strip the region and see if we find a match
            if '-' in lang:
                base_lang = lang.split('-')[0]
                try:
                    return LOCALE_CURRENCY_MAP[base_lang]
                except KeyError:
                    pass

    return 'usd'

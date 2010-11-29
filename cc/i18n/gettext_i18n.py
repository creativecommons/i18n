import os
import gettext
import pkg_resources


MO_PATH = pkg_resources.resource_filename(
    'cc.i18n', 'mo')
I18N_DOMAIN = 'cc_org'
CCORG_GETTEXT_TRANSLATIONS = {}


def translations_for_locale(locale, mo_path=MO_PATH):
    """
    Get the right translation and return it
    """
    cache_key = (locale, mo_path)
    if CCORG_GETTEXT_TRANSLATIONS.has_key(cache_key):
        return CCORG_GETTEXT_TRANSLATIONS[cache_key]

    # do I have the order backwards here?
    langs = [locale]
    if '_' in locale:
        root_lang = locale.split('_')[0]
        if os.path.exists(os.path.join(mo_path, root_lang)):
            langs.append(root_lang)

    if not 'en' in langs:
        langs.append('en')

    translations = None

    for lang in langs:
        mo_path = os.path.join(MO_PATH, lang, 'LC_MESSAGES', 'cc_org.mo')
        if not os.path.exists(mo_path):
            continue

        this_trans = gettext.GNUTranslations(open(mo_path, 'rb'))

        if translations is None:
            translations = this_trans
        else:
            translations.add_fallback(this_trans)

    CCORG_GETTEXT_TRANSLATIONS[cache_key] = translations
    return translations


def ugettext_for_locale(locale, mo_path=MO_PATH):
    def _wrapped_ugettext(message):
        return translations_for_locale(
            locale, mo_path).ugettext(message).decode('utf-8')

    return _wrapped_ugettext

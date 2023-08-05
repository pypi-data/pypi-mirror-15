from django import template

from molo.core.models import Page, SiteLanguage, ArticlePage, SectionPage

register = template.Library()


@register.inclusion_tag(
    'core/tags/section_listing_homepage.html',
    takes_context=True
)
def section_listing_homepage(context):
    request = context['request']
    locale_code = context.get('locale_code')

    if request.site:
        sections = request.site.root_page.specific.sections()
    else:
        sections = []

    return {
        'sections': [
            a.get_translation_for(locale_code) or a for a in sections],
        'request': context['request'],
        'locale_code': locale_code,
    }


@register.inclusion_tag(
    'core/tags/latest_listing_homepage.html',
    takes_context=True
)
def latest_listing_homepage(context, num_count=5):
    request = context['request']
    locale_code = context.get('locale_code')

    if request.site:
        articles = request.site.root_page.specific\
            .latest_articles()[:num_count]
    else:
        articles = []

    return {
        'articles': [
            a.get_translation_for(locale_code) or a for a in articles],
        'request': context['request'],
        'locale_code': locale_code,
    }


@register.inclusion_tag('core/tags/bannerpages.html', takes_context=True)
def bannerpages(context):
    request = context['request']
    locale_code = context.get('locale_code')

    if request.site:
        pages = request.site.root_page.specific.bannerpages()
    else:
        pages = []

    return {
        'bannerpages': [
            a.get_translation_for(locale_code) or a for a in pages],
        'request': context['request'],
        'locale_code': locale_code,
    }


@register.inclusion_tag('core/tags/footerpage.html', takes_context=True)
def footer_page(context):
    request = context['request']
    locale_code = context.get('locale_code')

    if request.site:
        pages = request.site.root_page.specific.footers()
    else:
        pages = []

    return {
        'footers': [a.get_translation_for(locale_code) or a for a in pages],
        'request': context['request'],
        'locale_code': locale_code,
    }


@register.inclusion_tag('core/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    locale_code = context.get('locale_code')

    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.live().ancestor_of(
            self, inclusive=True).filter(depth__gt=3).specific()

    translated_ancestors = []
    for p in ancestors:
        if hasattr(p, 'get_translation_for'):
            translated_ancestors.append(
                p.get_translation_for(locale_code) or p)
        else:
            translated_ancestors.append(p)

    return {
        'ancestors': translated_ancestors,
        'request': context['request'],
    }


@register.inclusion_tag(
    'core/admin/translations_actions.html', takes_context=True)
def render_translations(context, page):
    if not hasattr(page.specific, 'get_translation_for'):
        return {}

    languages = [
        (l.locale, str(l))
        for l in SiteLanguage.objects.filter(is_main_language=False)]

    return {
        'translations': [{
            'locale': {'title': title, 'code': code},
            'translated':
                page.specific.get_translation_for(code, is_live=None)
            if hasattr(page.specific, 'get_translation_for') else None}
            for code, title in languages],
        'page': page
    }


@register.assignment_tag(takes_context=True)
def load_descendant_articles_for_section(
        context, section, featured_in_homepage=None, featured_in_section=None,
        featured_in_latest=None, count=5):
    '''
    Returns all descendant articles (filtered using the parameters)
    If the `locale_code` in the context is not the main language, it will
    return the translations of the live articles.
    '''
    page = section.get_main_language_page()
    locale = context.get('locale_code')

    qs = ArticlePage.objects.live().descendant_of(page).filter(
        languages__language__is_main_language=True)

    if featured_in_homepage is not None:
        qs = qs.filter(featured_in_homepage=featured_in_homepage)

    if featured_in_latest is not None:
        qs = qs.filter(featured_in_latest=featured_in_latest)

    if featured_in_section is not None:
        qs = qs.filter(featured_in_section=featured_in_section)

    if not locale:
        return qs[:count]

    return [a.get_translation_for(locale) or a for a in qs[:count]]


@register.assignment_tag(takes_context=True)
def load_child_articles_for_section(context, section, count=5):
    '''
    Returns all child articles
    If the `locale_code` in the context is not the main language, it will
    return the translations of the live articles.
    '''
    page = section.get_main_language_page()
    locale = context.get('locale_code')

    qs = ArticlePage.objects.live().child_of(page).filter(
        languages__language__is_main_language=True)

    if not locale:
        return qs[:count]

    return [a.get_translation_for(locale) or a for a in qs[:count]]


@register.assignment_tag(takes_context=True)
def load_child_sections_for_section(context, section, count=5):
    '''
    Returns all child articles
    If the `locale_code` in the context is not the main language, it will
    return the translations of the live articles.
    '''
    page = section.get_main_language_page()
    locale = context.get('locale_code')

    qs = SectionPage.objects.live().child_of(page).filter(
        languages__language__is_main_language=True)

    if not locale:
        return qs[:count]

    return [a.get_translation_for(locale) or a for a in qs[:count]]

import logging
import re
import requests
import time
from bs4 import BeautifulSoup

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


LONGPOST_HEIGHT_MIN = 1000
BASE_URL = 'http://9gag.com/'

_sections = None
_cache = dict() # type: dict[str, tuple[int, dict]]

logger = logging.getLogger('pyninegag')

# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# logger.addHandler(ch)

class NineGagError(Exception): pass


class UnknownArticleType(NineGagError): pass


class NotSafeForWork(NineGagError): pass


def _bs_from_response(html):
    """
    Returns BeautifulSoup from given str with html inside.

    :param str html:
    :rtype: bs4.BeautifulSoup
    """
    return BeautifulSoup(html, "html.parser")


def _bs_from_url(url):
    """
    Returns BeautifulSoup from given url.
    Shortcut function.

    :param str url:
    :rtype: bs4.BeautifulSoup
    """
    return _bs_from_response(requests.get(url).text)


def get_sections():
    """
    Return dict of 9gag sections, where keys are capitalized sections names, and values are their urls.
    Caches returning value.

    :rtype: dict
    """
    global _sections
    if _sections is None:
        bs = _bs_from_url(BASE_URL)
        l = bs.find(attrs='nav-menu').find(attrs='primary').find_all('li')[1:-1]
        l.extend(bs.find_all(attrs="badge-section-menu-items"))
        _sections = dict((i.a.text.strip(), i.a['href']) for i in l)
    return _sections


def _get_gif(container):
    """
    Return dict with key url that will contain url to source gif and type with value "gif".

    :param bs4.Tag container:
    :rtype: dict
    """
    tag = container.find(attrs='badge-animated-container-animated')
    if not tag:
        return None
    return {'url': tag['data-image'], 'type': 'gif'}


def _get_image(container):
    """
    Return dict with key url that will contain url to source image and type with value image,
    if source image height is below 1000, or longpost, otherwize.

    :param bs4.Tag container:
    :rtype: dict
    """
    tag = container.find(attrs='badge-item-img')
    if not tag:
        return None

    style = container.a['style']
    match = re.search(r'[\d\.]+', style)
    if not match:
        return
    height = float(match.group())

    type = 'image'
    if height > LONGPOST_HEIGHT_MIN:
        type = 'longpost'

    url = urlparse.urljoin(BASE_URL, container.a['href'])

    bs = _bs_from_url(url)
    tag = bs.find(attrs='badge-item-img')

    return {'url': tag['src'], 'type': type}


def _cache_article(func):
    """
    I wanted to use functools.lru_cache here, but it is not compatible with python 2.7 :(

    :param dict article:
    :rtype: dict
    """
    def wrapper(article):
        if article['id'] in _cache:
            return _cache[article['id']][1]
        else:
            data = func(article=article)
            _cache[article['id']] = (time.time(), data)
            if len(_cache) > 100:
                ordered_keys = sorted(_cache.keys(), key=lambda key: _cache[key][0])
                list(map(_cache.pop, ordered_keys[:20]))
            return data

    return wrapper


@_cache_article
def _get_data(article):
    """
    Return article data. Returns dict with keys url and type.

    :param bs4.Tag article:
    :rtype: dict|None
    """
    container = article.find(attrs='badge-post-container')
    if container is None:
        raise NotSafeForWork()
    return _get_gif(container) or _get_image(container)


def _parse_article(article):
    """
    Return parsed article data. Supported keys: id, url, votes, comments, title, data.

    :param bs4.Tag article:
    :rtype: dict|None
    """
    data = dict()
    data['id'] = article['data-entry-id']
    data['url'] = article['data-entry-url']
    data['votes'] = article['data-entry-votes']
    data['comments'] = article['data-entry-comments']
    data['title'] = article.find(attrs='badge-item-title').a.text.strip()
    try:
        data['data'] = _get_data(article)
    except NotSafeForWork:
        logger.debug('NSFW Post: {} {}'.format(data['id'], data['url']))
        return
    if not data['data']:
        logger.warning('Unknown article type of {}: {}'.format(data['id'], data['url']))
        return
    return data


def _paginated_url(url, max_pages=1):
    """
    :param int|None max_pages: how many pages of results to parse. If None - all available. Default 1 - only first page.
    :rtype: collections.Iterable[tuple[str, dict]]
    """
    parsed_pages = 0
    while max_pages is None or (max_pages and parsed_pages < max_pages):
        parsed_pages += 1

        response = requests.get(url, headers={'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'})
        json = response.json()

        if not len(json['ids']): break

        url = urlparse.urljoin(BASE_URL, json['loadMoreUrl'])

        for article_id in json['ids']:
            yield article_id, json['items'][article_id]


def get_articles(url, max_pages=1, raise_on_error=False):
    """
    Return iterable with all articles found on given url.

    :param str url:
    :param int|None max_pages: how many pages of results to parse. If None - all available. Default 1 - only first page.
    :rtype: collections.Iterable[dict]
    """
    for article_id, article in _paginated_url(url, max_pages=max_pages):
        try:
            data = _parse_article(_bs_from_response(article).article)
            if not data:
                logger.debug('Empty data for {}'.format(article_id))
                continue
            yield data
        except Exception as e:
            logger.exception('Error while parsing article {}'.format(article_id))
            if raise_on_error:
                raise


def get_by_section(section_name, max_pages=1):
    """
    Return iterable with all articles found in given section.

    :param str section_name:
    :param int|None max_pages: how many pages of results to parse. If None - all available. Default 1 - only first page.
    :rtype: collections.Iterable[dict]
    """
    sections = get_sections()
    if section_name not in sections:
        raise ValueError('Invalid section name {}. Should be one of: {}'.format(section_name, list(sections.keys())))
    return get_articles(sections[section_name], max_pages=max_pages)

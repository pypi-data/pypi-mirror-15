from Acquisition import aq_inner
from ftw.solr import _
from ftw.solr.interfaces import ILiveSearchSettings
from itertools import groupby
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.PythonScripts.standard import html_quote
from Products.PythonScripts.standard import url_quote_plus
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
import json


def quotestring(s):
    return '"%s"' % s


def quote_bad_chars(s):
    bad_chars = ["(", ")"]
    for char in bad_chars:
        s = s.replace(char, quotestring(char))
    return s


class FtwSolrLiveSearchReplyView(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        q = self.request.form.get('term', None)
        self.limit = int(self.request.form.get('limit', 10))
        path = self.request.form.get('path', None)

        plone_utils = getToolByName(context, 'plone_utils')
        self.pretty_title_or_id = plone_utils.pretty_title_or_id
        self.normalizeString = plone_utils.normalizeString
        plone_view = getMultiAdapter((context, self.request), name='plone')
        self.get_icon = plone_view.getIcon

        pprops = getToolByName(context, 'portal_properties')
        sprops = getattr(pprops, 'site_properties', None)
        self.useViewAction = []
        if sprops is not None:
            self.useViewAction = sprops.getProperty('typesUseViewActionInListings',
                                                    [])

        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ILiveSearchSettings)

        # XXX really if it contains + * ? or -
        # it will not be right since the catalog ignores all non-word
        # characters equally like
        # so we don't even attept to make that right.
        # But we strip these and these so that the catalog does
        # not interpret them as metachars
        # See http://dev.plone.org/plone/ticket/9422 for an explanation of
        # '\u3000'
        multispace = u'\u3000'.encode('utf-8')
        for char in ('?', '-', '+', '*', multispace):
            q = q.replace(char, ' ')
        r = quote_bad_chars(q) + '*'
        self.searchterms = url_quote_plus(r)

        site_encoding = plone_utils.getSiteEncoding()
        if path is None:
            path = getNavigationRoot(context)
        catalog = getToolByName(context, 'portal_catalog')
        friendly_types = plone_utils.getUserFriendlyTypes()

        self.facet_params = context.restrictedTraverse(
            '@@search-facets/facet_parameters')()

        self.searchterm_query = '?searchterm=%s' % url_quote_plus(q)

        if self.settings.grouping:
            results = catalog(SearchableText=r, portal_type=friendly_types,
                              request_handler='livesearch', path=path,
                              sort_limit=self.settings.group_search_limit)[:self.settings.group_search_limit]

        else:
            results = catalog(SearchableText=r, portal_type=friendly_types,
                              request_handler='livesearch', path=path,
                              sort_limit=self.limit)[:self.limit]

        self.request.response.setHeader(
            'Content-Type', 'application/json;charset=%s' % site_encoding)

        return self.get_results_as_json(results)

    def get_results_as_json(self, results):
        if self.settings.grouping:
            grouped_results = []

            group_func = lambda result: result['portal_type']

            def sort_func(item):
                group_by = self.settings.group_by
                try:
                    return group_by.index(item['portal_type'])
                except ValueError:
                    return len(group_by) + 1

            results = sorted(results, key=sort_func)

            group_limit = self.settings.group_limit

            for portal_type, group in groupby(results, group_func):

                if group_limit:
                    group = list(group)[:self.settings.group_limit]
                else:
                    group = list(group)

                group[0]['first_of_group'] = True
                grouped_results.extend(group)

            return json.dumps(self.generate_items(grouped_results))

        else:
            return json.dumps(self.generate_items(results))

    def generate_items(self, results):
        data = []
        for result in results:
            url = result.getURL()
            if result.portal_type in self.useViewAction:
                url += '/view'
            url = url + self.searchterm_query
            title = self.get_title(result)
            first_of_group = 'first_of_group' in result and result.first_of_group

            # XXX Typestools lookup could be cacheable
            types_tool = api.portal.get_tool('portal_types')

            type_domain = types_tool.get(result.portal_type).i18n_domain

            # XXX Somehow solr does not return the "Type" for Files - The
            # binary adder explicitly ignores this attr.
            if result.portal_type == 'File':
                portal_type = translate(result.portal_type,
                                        domain=type_domain,
                                        context=self.request)
            else:
                portal_type = translate(result.Type,
                                        domain=type_domain,
                                        context=self.request)

            data.append({'icon': self.get_icon(result).html_tag() or '',
                         'url': url,
                         'title': title,
                         'description': self.get_description(result),
                         'cssclass': self.get_css_class(result),
                         'type': portal_type,
                         'firstOfGroup': first_of_group
                         })

        if(len(data)):
            data.append(self.get_show_more_item())
        else:
            data.append(self.get_nothing_found_item())

        search_help_link = self.get_search_help_item()
        if search_help_link:
            data.append(self.get_search_help_item())

        return data

    def get_title(self, brain):
        return safe_unicode(self.pretty_title_or_id(brain))

    def get_description(self, brain):
        display_description = safe_unicode(brain.Description)
        # need to quote it, to avoid injection of html containing javascript
        # and other evil stuff
        return html_quote(display_description)

    def get_css_class(self, brain):
        return 'contenttype-{0}'.format(
            self.normalizeString(brain.portal_type))

    def get_search_help_item(self):
        label_search_help = _('label_search_help', default='Search help')
        search_help_obj = api.portal.get_navigation_root(
            self.context).restrictedTraverse('searchhelp', None)

        if search_help_obj is None:
            return None

        return {
            'url': search_help_obj.absolute_url(),
            'title': translate(label_search_help, context=self.request),
            'first_of_group': False,
            'cssclass': 'no-result'
            }

    def get_show_more_item(self):
        label_show_all = _('label_show_all', default='Show all items')
        params = self.facet_params
        params += '&SearchableText=' + self.searchterms
        path = self.request.form.get('path', None)
        if path:
            params += '&path=' + url_quote_plus(path)
        url = '@@search?{0}'.format(params)

        return {
            'url': url,
            'title': translate(label_show_all, context=self.request),
            'first_of_group': False,
            'cssclass': 'no-result'
        }

    def get_nothing_found_item(self):
        label_nothing_found = _('label_nothing_found',
                                default='No items found')
        params = self.facet_params
        params += '&SearchableText=' + self.searchterms
        path = self.request.form.get('path', None)
        if path:
            params += '&path=' + url_quote_plus(path)
        url = '@@search?{0}'.format(params)

        return {
            'url': url,
            'title': translate(label_nothing_found, context=self.request),
            'first_of_group': False,
            'cssclass': 'no-result'
        }

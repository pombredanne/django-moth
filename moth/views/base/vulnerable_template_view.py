import urlparse

from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from moth.utils.plugin_families import get_plugin_families


class VulnerableTemplateView(TemplateView):
    '''
    All vulnerabilities inherit from this template, which will render the data
    returned by the subclasses, disable anti-CSRF, etc.
    '''
    # The template to use to render this view
    template_name = "moth/vulnerability-output.html"
    
    # The title that will appear on the rendered HTML
    title = None
    
    # The description that will appear on the rendered HTML
    description = None
    
    # The URL pattern string (not regex for now) which we'll try to match before
    # sending information to this view. This is parsed by the router view.
    url_path = None
    
    # Is this a real vulnerability or a false positive check?
    false_positive_check = False
    
    # You can provide tags to a vulnerability, such as trivial, POST, GET,
    # high risk, hacme, etc.
    tags = []
    
    # URLs to interesting/related information
    references = []
    
    # Add link to this view from the index?
    linked = True
    
    plugin_families = set(get_plugin_families())
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(VulnerableTemplateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(VulnerableTemplateView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['description'] = self.description
        context['false_positive_check'] = self.false_positive_check
        context['tags'] = self.tags
        context['references'] = self.references
        return context

    def get_url_path(self):
        '''
        :return: The URL path, without any query string. To be used mainly in
                 routing to the right view without taking parameters (?text=1)
                 into account.
        '''
        return urlparse.urlparse(self.url_path).path
    
    def get_family_plugin(self):
        '''
        :param view_obj: A view object, an instance of (for example) 
                         moth.views.vulnerabilities.audit.xss.SimpleXSSView
        :return: A string containing the plugin family name, for the previous
                 input it would be 'audit'.
        '''
        module_name = self.__module__
        split_mname = module_name.split('.')
        
        family = list(self.plugin_families.intersection(set(split_mname)))[0]
        plugin = split_mname[split_mname.index(family) + 1]
        
        return family, plugin 

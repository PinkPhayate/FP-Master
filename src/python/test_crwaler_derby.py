import crawler_derby as cd
from urllib import request
import lxml


def test_find_bug_module():
    url = 'https://issues.apache.org//jira/secure/attachment/12551717/SOLR-4019.patch'
    source = request.urlopen(url)
    modules = cd.extract_bug_module_name(source)
    print(modules)

def test_skip_versions():
    url = 'https://lucene.apache.org/solr/7_0_1/changes/Changes.html'
    url_json = cd.get_fixed_bug_url(url)
    print('before size: {}'.format(len(url_json.keys())))
    url_json = cd.skip_version(url_json)
    print('after size: {}'.format(len(url_json.keys())))

def test_get_bug_module():
    url = 'https://issues.apache.org//jira/secure/attachment/12551717/SOLR-4019.patch'
    modules = cd.extract_bug_module_name(url)
    print(modules)


# test_find_bug_module()
# test_skip_versions()
test_get_bug_module()

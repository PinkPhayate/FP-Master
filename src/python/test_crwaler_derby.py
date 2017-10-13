import crawler_solr as cs
from urllib import request
import lxml


def test_skip_versions():
    url = 'https://lucene.apache.org/solr/7_0_1/changes/Changes.html'
    url_json = cs.get_fixed_bug_url(url)
    print('before size: {}'.format(len(url_json.keys())))
    url_json = cs.skip_version(url_json)
    print('after size: {}'.format(len(url_json.keys())))

def test_get_bug_module():
    url = 'https://issues.apache.org//jira/secure/attachment/12551717/SOLR-4019.patch'
    modules = cs.extract_bug_module_name(url)
    print(modules)

def test_find_bug_module():
    url = 'https://issues.apache.org/jira/browse/SOLR-10279'
    li = cs.find_bug_module(url)
    print(li)


# test_skip_versions()
# test_get_bug_module()
test_find_bug_module()

import crawler_derby as cd
from urllib import request
import lxml


def test_find_bug_module():
    url = 'https://issues.apache.org/jira/secure/attachment/12861732/SOLR_10404.patch'
    source = request.urlopen(url)
    modules = cd.extract_bug_module_name(source)
    print(modules)

test_find_bug_module()

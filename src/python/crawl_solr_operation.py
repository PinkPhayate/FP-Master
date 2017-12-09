import crawler_solr as cs
import sys

skip_array = ['v6.5.1', 'v1.1.0', 'v4.10.3', 'v4.5.0', 'v4.10.4',
              'v4.0.0-alpha', 'v6.6.0', 'v3.1.0', 'v4.0.0-beta',
              'v1.4.0', 'v4.4.0',
              'v4.2.0', 'v5.3.0', 'v4.10.2', 'v5.3.1', 'v5.5.0', 'v5.4.1',
              'v3.6.0', 'v1.2.bug_fixes', 'v4.3.1', 'v3.5.0', 'v6.4.1',
              'v4.10.0', 'v7.0.1', 'v6.1.0', 'v6.2.0', 'v4.7.2', 'v6.4.2',
              'v4.7.0', 'v5.0.0', 'v5.1.0', 'v6.2.1', 'v3.4.0', 'v4.0.0',
              'v4.10.1', 'v4.6.0', 'v3.6.2', 'v5.2.1', 'v4.7.1', 'v4.9.0']

specified_versions = ['v7.0.0', 'v6.5.0', 'v6.5.1', 'v6.6.0',
                      'v6.4.0', 'v6.4.1', 'v6.4.2', 'v6.5.0']
def skip_version(url_json):
    popped_url_json = url_json.copy()
    for version in url_json.keys():
        if version in skip_array:
            del popped_url_json[version]
    return popped_url_json

def select_specified_version(url_json, specifed_version):
    new_json = {}
    new_json[specifed_version] = url_json[specifed_version]
    return new_json

def select_specified_versions(url_json):
    new_json = {}
    for version in url_json.keys():
        if version in specified_versions:
            new_json[version] = url_json[version]
    return new_json

def main():
    url = 'https://lucene.apache.org/solr/7_0_1/changes/Changes.html'
    url_json = cs.get_fixed_bug_url(url)
    url_json = skip_version(url_json)
    cs.crawl_versions(url_json)

def operate_specidied_version(specifed_version=None):
    print('crawl bug report of the specified version')
    url = 'https://lucene.apache.org/solr/7_0_1/changes/Changes.html'
    origin_json = cs.get_fixed_bug_url(url)
    url_json = {}
    if specifed_version is None:
        url_json = select_specified_versions(origin_json)
    else:
        url_json = select_specified_version(origin_json, specifed_version)
    cs.crawl_versions(url_json)


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        main()
    elif args[1] == 'spec':
        version = None if len(args) == 2 else args[2]
        operate_specidied_version(version)

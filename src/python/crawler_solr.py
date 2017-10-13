import lxml
from bs4 import BeautifulSoup
import sys
from urllib import request
import configparser
from multiprocessing import Process
from tqdm import tqdm

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')

PATCH_DOMAIN_URL = 'https://issues.apache.org'
MODULE_POST_STRING = '.java'
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Solr/bug'


def export_bug_modules(version, module_set):
    filename = '{}/slr_{}_bgmd.csv'.format(METRICS_DIR, version[1:])
    with open(filename, mode='w', encoding='utf-8') as fh:
        for module in module_set:
            fh.write('{}\n'.format(module))

def export_error_log(lines):
    with open('./log/export_error.log', mode='w', encoding='utf-8') as fh:
        for line in lines:
            fh.write('{}\n'.format(line))

def get_fixed_bug_url(url):
    def __extract_version_num(attr_text):
        array = attr_text.split('.')
        return '.'.join(array[:3])

    source = request.urlopen(url)
    soup = BeautifulSoup(source, "lxml")
    url_dict = {}
    for ol in soup.findAll('ol'):
        attr_text = ol.attrs['id']
        if 'bug_fixes.list' in attr_text:
            version_num = __extract_version_num(attr_text)
            url_list = []
            for li in ol.findAll("li"):
                for link in li.findAll('a'):
                    url = link.attrs['href']
                    url_list.append(url)
                url_dict[version_num] = url_list
    return url_dict

def get_patch_file_url(url):
    source = request.urlopen(url)
    soup = BeautifulSoup(source, "lxml")
    patch_urls = []
    for div in soup.findAll("div", attrs={"attachment-thumb"}):
        for link in div.findAll('a'):
            url = link.attrs['href']
            patch_urls.append(url)
    return patch_urls

def extract_bug_module_name(patch_url):
    def __is_modified_line(line):
        if len(line) < 3:
            return False
        line = line.decode('utf-8')
        prim_string = line[:3]
        if prim_string != '---':
            return False
        if MODULE_POST_STRING not in line:
            return False
        return True

    def __extract_module_name(line):
        module_name = line.split(' ')[1]
        return module_name.rsplit(MODULE_POST_STRING)[0] + MODULE_POST_STRING

    source = request.urlopen(patch_url)
    lines = source.readlines()
    modules = []
    for idx, line in enumerate(lines):
        try:
            if __is_modified_line(line):
                module_name = __extract_module_name(line.decode('utf-8'))
                modules.append(module_name)
        except Exception:
            lines = []
            lines.append('[ERROR] this line couldnt convert unicode')
            lines.append('patch_url: {}, line: {}'.format(patch_url, idx))
            lines.append('file content: {}'.format(line))
            export_error_log(lines)
    return modules

def find_bug_module(url):
    bug_module_map = []
    try:
        patch_urls = get_patch_file_url(url)
    except:
        print('this bug report couldnt be read patch files, url: {}'
              .format(url))
        return []
    for patch_url in patch_urls:
        patch_url = '{}/{}'.format(PATCH_DOMAIN_URL, patch_url)
        try:
            modules = extract_bug_module_name(patch_url)
            bug_module_map.extend(modules)
        except:
            print('[ERROR] this patch file could not open: {}'
                  .format(patch_url))

    return list(set(bug_module_map))

def crawl_versions(url_json):
    print('[INFO] versions: {}'.format(url_json.keys()))
    for version, url_array in url_json.items():
        jobs = []
        modules = []
        print('[INFO] start to extract fixed module of {} '.format(version))
        print('[INFO] this version has {} fixed modules'
              .format(len(url_array)))
        for url in tqdm(url_array):
            module_set = find_bug_module(url)
            modules.extend(module_set)
        job = Process(target=export_bug_modules, args=(version, modules))
        jobs.append(job)
        job.start()
    [job.join() for job in jobs]

import csv
class VersionUtil:
    def __init__(self, version_file):
        self.version_file = version_file

    def get_version_list( self ) :
        dataReader = csv_reader = csv.reader(open(self.version_file, 'r'), delimiter=',', quotechar='"')
        list = []
        for row in dataReader :
            for index in row :
                list.append(index)
        return list.reverse()
    def get_all_previous_versions ( self, curr_version) :
        dataReader = csv_reader = csv.reader(open(self.version_file, 'r'), delimiter=',', quotechar='"')
        list = []
        flag = False
        for row in dataReader :
            list.append(row)
            if row == curr_version:
                flag = True
            if flag :
                break
        return list

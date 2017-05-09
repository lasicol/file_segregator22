import os
import argparse
import shutil
import time

current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
parser = argparse.ArgumentParser()
parser.add_argument('folder_path', type=str, help='You have to pass the path to folder which you want to clean up.')
args = parser.parse_args()




class Logger:
    def __init__(self, name='log.txt'):
        self.name = name
        self.f = open(self.name, 'w')
        self.f.write(current_time+'\n')
        self.warning_count = 0
        self.error_count = 0

    def add_to_log_info(self, line):
        self.f.write('[INFO]  ' + line + '\n')
        print('[INFO]  ' + line)

    def add_to_log_error(self, line):
        self.f.write('[ERROR]  ' + line + '\n')
        print('[ERROR]  ' + line)
        self.error_count += 1

    def add_to_log_warning(self, line):
        self.f.write('[WARNING]  ' + line + '\n')
        print('[WARNING]  ' + line)
        self.warning_count += 1

    def __del__(self):
        self.f.write('\nErrors: {0}, warning: {1} \n'.format(self.error_count, self.warning_count))
        print('\n Errors: {0}, warnings: {1} '.format(self.error_count, self.warning_count))
        self.f.close()


class Folder:
    def __init__(self, path):
        """
        The class has been made to menage files in given folder.

        """
        self.path = path
        self.list_of_files = []
        self.log_file_name = 'log.txt'
        self.log = Logger(os.path.join(self.path, self.log_file_name))

    def check_files_in_folder(self) -> None:
        self.list_of_files = [file for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file))]

    def group_by_extension(self) -> None:
        if not len(self.list_of_files)-1:
            self.log.add_to_log_error('No files in given directory...: ' + self.path)
            self.log.add_to_log_info('The program is terminated.')
            exit(1)
        else:
            for i in self.list_of_files:
                splitted_str = i.split(sep='.')
                folder_name = '___' + splitted_str[-1]
                if i == self.log_file_name:
                    continue
                if len(splitted_str) < 2:
                    folder_name = '___noExtension'
                try:
                    os.makedirs(os.path.join(self.path, folder_name))
                except OSError:
                    self.log.add_to_log_info("Folder '{0}' is already exist.".format(folder_name))
                try:
                    shutil.move(os.path.join(self.path, i), os.path.join(self.path, folder_name))
                    self.log.add_to_log_info("File {0} has been moved to {1}".format(i, folder_name))
                except shutil.Error:
                    self.log.add_to_log_warning("Cannot move file {0} to folder {1}".format(i, folder_name))


def main():
    folder = Folder(args.folder_path)
    folder.check_files_in_folder()
    folder.group_by_extension()


if __name__ == '__main__':
    main()

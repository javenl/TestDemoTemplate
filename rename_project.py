# coding:utf-8

import os
import sys
import re
import fileinput

replce_extensions = [
  '.xcworkspace',
  '.pbxproj',
  '.podspec',
  '.xcworkspacedata'
]

replace_filename = [
  'Podfile',
  'readme.md'
]


def check_path_exist(dir):
  if not os.path.exists(dir):
    print '%s 路径不存在' % dir
    exit()


def fine_projectname(project_dir):
  origin_project_name = None
  subfiles = os.listdir(project_dir)
  for filename in subfiles:
    file_extension = os.path.splitext(filename)[1]
    if file_extension == '.xcodeproj':
      origin_project_name = os.path.splitext(filename)[0]

  if origin_project_name == None:
    print '%s目录下找不到 .xcodeproj文件' % project_path
    exit()
  return origin_project_name

if __name__ == '__main__':

    project_dir = None
    renamed_project_name = None
    origin_project_name = None

    if len(sys.argv) == 3:
      project_dir = sys.argv[1]
      check_path_exist(project_dir)
      origin_project_name = fine_projectname(project_dir)
      renamed_project_name = sys.argv[2]
    else:
      project_dir = raw_input('输入项目目录路径:\n')
      check_path_exist(project_dir)
      origin_project_name = fine_projectname(project_dir)
      renamed_project_name = raw_input('把 %s 项目重命名为:\n' % origin_project_name)


    # Test Data
    # project_dir = '/Users/liu/Desktop/TestProjects/TestDemo/'
    # renamed_project_name = 'TestDemo6'

    print '!!!请确保代码已全部提交,以便UnDo!!!'
    print '!!!工程将从 %s 重命名为 %s!!!' % (origin_project_name, renamed_project_name)
    y = raw_input('\n输入Y/y确认操作:')
    if y != 'y' and y != 'Y':
        exit()

    os.chdir(project_dir)

    print '删除xcuserdata'
    os.popen('rm -rf *.xcodeproj/xcuserdata')
    os.popen('rm -rf *.xcworkspace/xcuserdata')

    print '重名命目录'
    os.popen('mv %s %s' % (origin_project_name, renamed_project_name))
    os.popen('mv %s.xcodeproj %s.xcodeproj' % (origin_project_name, renamed_project_name))
    if os.path.exists('%s.podspec' % origin_project_name):
      os.popen('mv %s.podspec %s.podspec' % (origin_project_name, renamed_project_name))
    if os.path.exists('%s.xcworkspace' % origin_project_name):
      os.popen('mv %s.xcworkspace %s.xcworkspace' % (origin_project_name, renamed_project_name))
    if os.path.exists('%sTests' % origin_project_name):
      os.popen('mv %sTests %sTests' % (origin_project_name, renamed_project_name))

    print '重名命目录项目文件'
    for (dirpath, dirnames, filenames) in os.walk('.'):

        if dirpath.startswith('./.git') or dirpath.startswith('./Pods'):
            continue

        for filename in filenames:

            flag = False
            if filename in replace_filename:
                flag = True

            if not flag:
                file_extension = os.path.splitext(filename)[1]
                if file_extension in replce_extensions:
                    flag = True

            if not flag:
                continue

            filepath = os.path.abspath(os.path.join(dirpath, filename))
            for line in fileinput.input(filepath, inplace=True):
                if re.search(origin_project_name, line):
                    line = line.replace(origin_project_name, renamed_project_name)
                line = line.replace('\n', '')
                print line

    print '重命名成功'
    # os.popen('open %s.xcworkspace' % renamed_project_name)
    # os.popen('pod update --no-repo-update')

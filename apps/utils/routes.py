# coding:utf-8
"""
Name : routes.py
Author :lvyunze
Time : 2022/5/11 17:57
Desc : 扫描模块下的所有路由
"""
import platform
from importlib import import_module
from os.path import dirname, realpath
from glob import glob
apps_path = dirname(dirname(realpath(__file__)))
module_path = apps_path + '/modules'


class RouterHelper(object):
    def __init__(self):
        self.dirs_list = glob(f'{module_path}/*/api/v*')

    def find_api_file(self) -> list:
        """
        扫描api下的所有python文件并且找到路由，
        先扫描文件夹下是否有py文件后排除__init__文件，
        最后找py文件下的router，假如没有就pass掉
        :return:file_path
        """
        file_path = [each for api_path in self.dirs_list for each in glob(api_path+'/*.py')]
        # windows下的路径需要转换
        if platform.system() == "Windows":
            file_path = [each.replace('\\', '.') for api_path in self.dirs_list for each in glob(api_path+'/*.py')]
        file_path = [each for each in file_path if '__' not in each]
        file_path = [each.replace('.py', '').replace('/', '.') for each in file_path]
        file_path = [each[each.find('apps'):] for each in file_path]
        file_path_list = [{
            'module': each[each.find('modules.')+len('modules.'):each.find('api')-1],
            'name': each,
            'version': each[each.find('api.')+len('api.'):each.find('api.')+len('api.')+2],
        }for each in file_path]
        return file_path_list

    def file_router(self) -> list:
        api_file = self.find_api_file()
        router_list = []
        for each in api_file:
            params = import_module(each['name'])

            try:
                cls = getattr(params, "router")
                router_list.append({
                    'client': cls,
                    'module': each['module'],
                    'version': each['version']
                })
            except AttributeError:
                pass
        return router_list


if __name__ == '__main__':
    router = RouterHelper()
    router.file_router()

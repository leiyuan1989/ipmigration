# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 17:31:24 2025

@author: leiyuan
"""

from setuptools import find_packages, setup

setup(
    name='ipmigration',  # 模块名称
    version='0.1.0',      # 版本号
    packages= find_packages() ,  # 包含的Python包
    python_requires='>=3.9',  
    
    install_requires=[        
        'argparse',
        'setuptools>=50.0.0',
        'pytest>=7.4.0',
        #'docutils >= 0.3',
        #'Django >= 1.11, != 1.11.1, <= 2',
        #'requests[security, socks] >= 2.18.4',
        ],  

    author='ASTRI-ICET',  
    author_email='leiyuan@astri.org',
    description='ASTRI IP Migration Platform',  
    long_description=open('README.md', 'r').read(), 
    long_description_content_type='text/markdown', 
    url='https://github.com/leiyuan1989/ipmigration-doc',  # 项目主页
    classifiers=[  # 项目分类标签
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
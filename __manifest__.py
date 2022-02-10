# -*- coding: utf-8 -*-
{
    'name': 'Vehicle repair and maintenance service management software',
    'summary': """This is a management software""",
    'description': """
App Name
========
Something about the App.
    """,
    'version': '13.0.1.0',
    'author': 'MD AZHARUL AMIN MULLA',
    'website': 'http://www.company.com',
    'category': 'Tools',
    'sequence': 1,
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [

        ## Security
        'security/ir.model.access.csv',

        ## Report
        # 'reports/report_paper_format.xml',
        # 'reports/my_model_name_report.xml',
        
        ## Wizard
        # 'wizards/my_model_name_wizard.xml',
        
        ## View & Wizard
        'views/vehicle_info.xml',
        'views/services.xml',
        
    ],
    'qweb': [],
    'demo': [],
    'external_dependencies': {
        'python': [
            'werkzeug',
        ],
    },
    'icon': '/vehicle_management/static/description/car.png',
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0,
    'license': 'OPL-1',
        
}

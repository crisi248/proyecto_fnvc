# -*- coding: utf-8 -*-
{
    'name': "natacion",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', "sale"], 

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/categories_views.xml',
        'views/championships_views.xml',
        'views/club_views.xml',
        'views/sessions_views.xml',
        'views/sets_views.xml',          
        'views/styles_views.xml',
        'views/swimmers_views.xml',
        'views/tests_views.xml',      
        'views/views.xml',  
        'views/templates.xml',
        'demo/categories.xml',
        'demo/clubs.xml',
        'demo/swimmers.xml',
        'demo/cuota.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/categories.xml',
        'demo/clubs.xml',
        'demo/swimmers.xml',
        'demo/cuota.xml',
        'demo/demo.xml',
    ],
}


{
    'name': 'Hospital',
    'version': '15.0.1.0.1',
    'category': 'Category',
    'author': 'Vadim Mudruk',
    'website': 'https://github.com/Vadim-23',
    'license': 'Other proprietary',
    'depends': ['web', 'mail', ],
    'data': [
        'security/ir.model.access.csv',
        'data/data_disease.xml',

        'views/doctor_views.xml',
        'views/disease_views.xml',
        'views/patient_views.xml',
        'views/visit_views.xml',
        'views/menu_view.xml',
        'wizard/visit_patient_wizard_views.xml',
        'wizard/conducted_visit_wizard_views.xml',
        'report/report.xml',
        'report/visit_pacient_report.xml',
        'report/condacted_visit_report.xml',

    ],
    'demo': [
        'data/doctor_data.xml',
        'data/data_patiet.xml',
    ],
    'installable': True,
}

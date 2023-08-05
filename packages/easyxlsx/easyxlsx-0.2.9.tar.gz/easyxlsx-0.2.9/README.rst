=========================
easyxlsx
=========================

Base on xlsxwriter easy export excel


Version:
    0.2.2

Features:

* support Excel formats


Requirements
-----------

* Python 3.3+
* XlsxWriter>=0.8.5


Installation
------------

To install easyXlsx, simply:

.. code-block:: bash

    $ pip install easyxlsx


Example usage
-------------

.. code-block:: python

    from django.http import HttpResponse
    from easyxlsx import ModelExport, excel_response


    class UserExport(ModelExport):

        model = User
        fields = ('username', 'gender', 'age', 'email', 'added_at')


    class UserAdmin(admin.ModelAdmin):

        actions = ['export_action']

        def export_action(self, request, queryset):
            data = UserExport(queryset).export()

            content_type = 'application/vnd.ms-excel;charset=utf-8'
            response = HttpResponse(data, content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="download.xls"'
            return response



Contribute
----------

.. _`XlsxWriter`: https://github.com/jmcnamara/XlsxWriter

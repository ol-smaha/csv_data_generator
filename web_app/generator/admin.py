from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import HttpResponse, reverse, redirect

from .tasks import generate_csv
from .models import Schema, ColumnType, Column, DataSet


class ColumnInline(admin.TabularInline):
    model = Column
    extra = 1


class SchemaAdmin(admin.ModelAdmin):
    change_list_template = "schema_admin_page.html"
    list_display = ['title', 'modified_date']
    inlines = [ColumnInline]

    def get_urls(self):
        urls = super(SchemaAdmin, self).get_urls()
        custom_urls = [path('generate_csv/', self.generate_csv_view, name='generate_csv')]
        return custom_urls + urls

    @staticmethod
    def generate_csv_view(request):
        count = int(request.POST.get('count'))
        schema_pks = list(Schema.objects.values_list('pk', flat=True))
        data_pks = []

        for pk in schema_pks:
            d_set = DataSet.objects.create(schema_id=pk)
            data_pks.append(d_set.pk)

        generate_csv.delay(data_pks, count)

        return redirect(reverse('admin:index'))


class ColumnTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


class ColumnAdmin(admin.ModelAdmin):
    list_display = ['name', 'col_type', 'order']


class DataSetAdmin(admin.ModelAdmin):
    list_display = ['schema', 'created_date', 'colored_status', 'download_link']

    def get_urls(self):
        urls = super(DataSetAdmin, self).get_urls()
        custom_urls = [path('download-file/<int:pk>/', self.download_file, name='download_csv_dataset')]
        return custom_urls + urls

    def download_link(self, obj):
        if not obj.file_csv:
            return ''
        return format_html(
            '<a href="{}">Download file</a>',
            reverse('admin:download_csv_dataset', args=[obj.pk])
        )

    @staticmethod
    def download_file(request, pk):
        obj = DataSet.objects.get(pk=pk)
        with open(obj.file_csv.path, 'r') as file:
            response = HttpResponse(file, content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename={obj.file_csv}'
        return response

    def colored_status(self, object):
        color_dict = {
            'processing': 'yellow',
            'ready': 'lawngreen',
        }
        color = color_dict[object.status]
        return format_html(
            '<span style="background-color: {}">{}</span>',
            color, object.status
        )

    colored_status.admin_order_field = 'status'
    colored_status.short_description = 'Status'
    download_link.short_description = "Download file"


admin.site.register(Schema, SchemaAdmin)
admin.site.register(ColumnType, ColumnTypeAdmin)
admin.site.register(DataSet, DataSetAdmin)
# admin.site.register(Column, ColumnAdmin)

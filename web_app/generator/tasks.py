from __future__ import absolute_import, unicode_literals
import csv
from random import randint
from datetime import date

import names
import loremipsum
from django.core.files import File

from config.celery import app
from .models import DataSet


def gen_value(column, counter):
    if column.col_type.name == 'Integer':
        if column.range_from and column.range_to:
            return randint(column.range_from, column.range_to + 1)
        elif column.range_from:
            return randint(column.range_from, 10**4)
        elif column.range_to:
            return randint(0, column.range_to)
        else:
            return randint(0, 10**4)

    elif column.col_type.name == 'Text':
        if column.range_from and column.range_to:
            length = randint(column.range_from, column.range_to + 1)
            return loremipsum.generate(length, loremipsum.ParagraphLength.SHORT)
        elif column.range_from:
            length = randint(column.range_from, column.range_from + 10)
            return loremipsum.generate(length, loremipsum.ParagraphLength.SHORT)
        elif column.range_to:
            length = randint(5, column.range_to + 1)
            return loremipsum.generate(length, loremipsum.ParagraphLength.SHORT)
        else:
            return loremipsum.generate(2, loremipsum.ParagraphLength.SHORT)

    elif column.col_type.name == 'Email':
        return f'{names.get_last_name()}@dummy.com'

    elif column.col_type.name == 'Domain':
        return f'https://{column.name.lower()}_{counter}.com'

    elif column.col_type.name == 'Company':
        return f'{column.name.upper()}_{counter}'

    elif column.col_type.name == 'Full Name':
        return f'{names.get_full_name()}'

    elif column.col_type.name == 'Date':
        start_dt = date.today().replace(day=1, month=1).toordinal()
        end_dt = date.today().toordinal()
        random_day = date.fromordinal(randint(start_dt, end_dt))
        return f'{random_day}'

    else:
        return f'{column.name}_{counter}'


@app.task
def generate_csv(data_pks, count):
    data_qs = DataSet.objects.filter(pk__in=data_pks)

    for dataset in data_qs:
        filename = f'{dataset.schema.title}-{dataset.created_date.date()}-{dataset.pk}.csv'
        with open(f'./media/data_sets/{filename}', 'w+', newline='') as csv_file:
            columns = dataset.schema.column.all().order_by('order')
            fieldnames = [obj.name for obj in columns]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(count):
                rows = {col.name: gen_value(col, i) for col in columns}
                writer.writerow(rows)

            dataset.file_csv.save(filename, File(csv_file))
            dataset.status = 'ready'
            dataset.save()

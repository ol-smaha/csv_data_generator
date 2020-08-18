from django.db import models


class Schema(models.Model):
    title = models.CharField(max_length=128)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ColumnType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Column(models.Model):
    schema = models.ForeignKey(Schema,
                               on_delete=models.CASCADE,
                               related_name='column',
                               blank=True,
                               null=True)
    name = models.CharField(max_length=64)
    col_type = models.ForeignKey(ColumnType,
                                 on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    range_from = models.IntegerField(blank=True,
                                     null=True)
    range_to = models.IntegerField(blank=True,
                                   null=True)

    def __str__(self):
        return self.name


class DataSet(models.Model):
    STATUSES = (
        ('processing', 'Processing'),
        ('ready', 'Ready'),
    )
    schema = models.ForeignKey(Schema,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)
    status = models.CharField(max_length=32,
                              choices=STATUSES,
                              default=STATUSES[0][0])
    file_csv = models.FileField(upload_to='data_sets',
                                blank=True,
                                null=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.schema:
            return f'{self.schema.title}-{self.created_date}'
        return str(self.created_date)

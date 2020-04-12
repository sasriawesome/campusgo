
class AcademicActivity(Orderable, BaseModel):
    class Meta:
        verbose_name = _("Academic Activity")
        verbose_name_plural = _("Academic Activities")
        ordering = ('-date_start',)

    PENDING = 'PND'
    ONGOING = 'ONG'
    END = 'END'
    STATUS = (
        (PENDING, _('Pending')),
        (ONGOING, _('On Going')),
        (END, _('End')),
    )

    school_year = ParentalKey(
        SchoolYear, on_delete=models.PROTECT,
        related_name='academic_activities',
        verbose_name=_('Academic Year'))
    academic_year = ParentalKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='semester_activities',
        verbose_name=_('Semester Year'))
    date_start = models.DateField(
        verbose_name=_("Date start"))
    date_end = models.DateField(
        verbose_name=_("Date end"))
    activity = RichTextField(
        verbose_name=_("Activity"))
    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("RMU"),
        help_text=_("Resource Management Unit"))

    @property
    def status(self):
        list_date_start = (
            self.date_start.year,
            self.date_start.month,
            self.date_start.day
        )
        list_date_end = (
            self.date_end.year,
            self.date_end.month,
            self.date_end.day
        )
        activity_date_start = timezone.make_aware(
            timezone.datetime(*list_date_start))
        activity_date_end = timezone.make_aware(
            timezone.datetime(*list_date_end, hour=23, minute=59, second=59))

        cond1 = activity_date_start > timezone.make_aware(datetime.now())
        cond2 = activity_date_start <= timezone.make_aware(datetime.now()) <= activity_date_end
        cond3 = timezone.make_aware(datetime.now()) > activity_date_end

        if cond1:
            return AcademicActivity.STATUS[0][1]
        if cond2:
            return AcademicActivity.STATUS[1][1]
        if cond3:
            return AcademicActivity.STATUS[2][1]
        else:
            return 'Not Defined'

    def __str__(self):
        return "{} ({}/{})".format(
            self.academic_year,
            self.date_start.strftime('%d%m%Y'),
            self.date_end.strftime('%d%m%Y'),
        )

    def save(self, *args, **kwargs):
        self.school_year = self.academic_year.school_year
        super().save(*args, **kwargs)
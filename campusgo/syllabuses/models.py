
class LearningMaterialBlock(blocks.StructBlock):
    class Meta:
        icon = 'cogs'
        group = True
        template = 'modeladmin/campusgo_academic/syllabus/block/learning_material.html'

    name = blocks.CharBlock()
    description = blocks.CharBlock()
    type = blocks.ChoiceBlock(choices=[
        ('software', 'Software'),
        ('hardware', 'Hardware'),
        ('framework', 'Framework'),
        ('misc', 'Misc'),
    ], icon='cogs')


class ReferenceBlock(blocks.StructBlock):
    class Meta:
        icon = 'cogs'
        group = True
        template = 'modeladmin/campusgo_academic/syllabus/block/reference.html'

    title = blocks.CharBlock()
    description = blocks.TextBlock()
    type = blocks.ChoiceBlock(choices=[
        ('book', 'Book'),
        ('journal', 'Journal'),
        ('article', 'Article'),
        ('sourcecode', 'Source Code'),
        ('documentation', 'Documentation'),
        ('misc', 'Misc'),
    ], icon='cogs')


class Syllabus(ClusterableModel, NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _("Syllabus")
        verbose_name_plural = _("Syllabuses")

    title = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Name'))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='syllabuses',
        verbose_name=_('Course'))
    description = RichTextField(
        max_length=MaxLength.RICHTEXT.value,
        verbose_name=_('Description'))
    body = StreamField([
        ('topic', blocks.RichTextBlock(label="Topic", group=True)),
        ('competency', blocks.RichTextBlock(label="Competency", group=True)),
        ('learning_material', LearningMaterialBlock()),
        ('reference', ReferenceBlock())
    ])

    def generate_inner_id(self):
        form = [
            self.course.inner_id,
            str(self.reg_number).zfill(2)]
        self.inner_id = 'SIL.{}.{}'.format(*form)
        return self.inner_id

    def get_counter(self):
        custom_code = self.get_custom_code()
        ct_counter = Numerator.get_instance(self, custom_code=custom_code)
        return ct_counter

    def get_custom_code(self):
        form = [self.course.inner_id]
        return 'SIL.{}'.format(*form)

    def __str__(self):
        return self.title


class ProgramUnit(blocks.StructBlock):
    session = blocks.IntegerBlock()
    duration = blocks.IntegerBlock()
    topic = blocks.RichTextBlock()
    competency = blocks.RichTextBlock()


class LectureProgram(Orderable, NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _("Lecture Program")
        verbose_name_plural = _("Lecture Program")

    syllabus = ParentalKey(
        Syllabus, on_delete=models.CASCADE,
        related_name='lecture_programs',
        verbose_name=_('Syllabus'))
    programs = StreamField([
        ('program_unit', ProgramUnit())
    ])

    def generate_inner_id(self):
        form = [
            self.syllabus.inner_id,
            str(self.reg_number).zfill(2)]
        self.inner_id = 'SAP.{}.{}'.format(*form)
        return self.inner_id

    def get_counter(self):
        custom_code = self.get_custom_code()
        ct_counter = Numerator.get_instance(self, custom_code=custom_code)
        return ct_counter

    def get_custom_code(self):
        form = [self.syllabus.inner_id]
        return 'SAP.{}'.format(*form)

    def __str__(self):
        return self.inner_id

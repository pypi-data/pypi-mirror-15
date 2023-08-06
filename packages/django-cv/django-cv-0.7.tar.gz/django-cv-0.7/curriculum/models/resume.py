from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.utils.six import BytesIO
import qrcode
from qrcode.image.pure import PymagingImage

CURRICLUM_USER = getattr(settings, 'CURRICULUM_USER', '')


@python_2_unicode_compatible
class Resume(models.Model):
    firstname = models.CharField(max_length=150, verbose_name=_("First name"))
    lastname = models.CharField(max_length=150, verbose_name=_("Last name"))
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Title"))
    resume = models.TextField(max_length=3000, blank=True, null=True, verbose_name=_("resume"), help_text=_("Short profile's description"))
    image = models.ImageField(blank=True, null=True, verbose_name=_("image"))

    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("phone"))
    website = models.URLField(max_length=300, blank=True, null=True, verbose_name=_("website"))
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("email"))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("city"))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("country"))
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("address"))

    skill_summary = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("summary of skills"))
    experience_summary = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("summary of experience"))
    training_summary = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("summary of trainings"))
    project_summary = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("summary of projects"))

    driving_license = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("driving license"))
    hobbies = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("hobbies"))
    tags = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("tags"))

    skype = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Skype ID"))
    twitter = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Twitter"))
    linkedin = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("LinkedIn ID"))
    google = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Google+ ID"))
    stackoverflow = models.IntegerField(blank=True, null=True, verbose_name=_("StackOverflow ID"))
    github = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("GitHub ID"))
    flickr = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Flickr ID"))

    class Meta:
        app_label = 'curriculum'
        verbose_name = _("resume")

    def __str__(self):
        return "%s %s - %s" % (self.firstname, self.lastname, self.title)

    def create_website_qrcode(self):
        storage = get_storage_class(settings.DEFAULT_FILE_STORAGE)()
        img_name = '%s-webite-qrcode.png' % self.id
        img_file = BytesIO()
        img = qrcode.make(self.website, image_factory=PymagingImage)
        img.save(img_file)
        storage.save(img_name, img_file)

    def website_qrcode(self):
        storage = get_storage_class(settings.DEFAULT_FILE_STORAGE)()
        img_name = '%s-webite-qrcode.png' % self.id
        if not storage.exists(img_name):
            self.create_website_qrcode()
        return storage.url('%s-webite-qrcode.png' % self.id)


@python_2_unicode_compatible
class AbstractUserResumes(models.Model):
    user = models.ForeignKey(CURRICLUM_USER, unique=True, verbose_name=_("user"),
                             help_text=_("User associated with resume."))
    resumes = models.ManyToManyField(Resume)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s resume(s)' % self.user

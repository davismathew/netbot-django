from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.template.defaultfilters import slugify
import markdown


class ConfTemplate(models.Model):
    ACTIVE = 'A'
    DELETED = 'D'
    STATUS = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )

    name = models.CharField(max_length=255,null=True,default="Something")
    description = models.TextField(max_length=4000)
    variable = models.TextField(null=True)
    template = models.TextField(null=True)
    helptext = models.TextField(null=True)
    status = models.CharField(max_length=1, choices=STATUS, default=ACTIVE)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True,
                                    related_name="+")

    class Meta:
        verbose_name = _("ConfTemplate")
        verbose_name_plural = _("ConfTemplates")
        # ordering = ("-create_date",)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(ConfTemplate, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        super(ConfTemplate, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    @staticmethod
    def get_published():
        conftemplates = ConfTemplate.objects.filter(status=ConfTemplate.ACTIVE)
        return conftemplates


class ConfTemplateInstance(models.Model):
    name = models.CharField(max_length=255,null=True,default="Something")
    varvalues = models.TextField(null=True)
    conftemplate = models.ForeignKey(ConfTemplate, null=True)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True,
                                    related_name="+")
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("ConfTemplateInstance")
        verbose_name_plural = _("ConfTemplateInstances")

    def save(self, *args, **kwargs):
        if not self.pk:
            super(ConfTemplateInstance, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        super(ConfTemplateInstance, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')


    # @staticmethod
    # def get_published():
    #     tasks = Conf.objects.filter(status=Task.ACTIVE)
    #     return tasks
    #
    # def create_tags(self, tags):
    #     tags = tags.strip()
    #     tag_list = tags.split(' ')
    #     for tag in tag_list:
    #         if tag:
    #             t, created = Tag.objects.get_or_create(tag=tag.lower(),
    #                                                    article=self)
    #
    # def get_tags(self):
    #     return Tag.objects.filter(article=self)

    # def get_summary(self):
    #     if len(self.content) > 255:
    #         return u'{0}...'.format(self.content[:255])
    #     else:
    #         return self.content
    #
    # def get_summary_as_markdown(self):
    #     return markdown.markdown(self.get_summary(), safe_mode='escape')

    # def get_comments(self):
    #     return ArticleComment.objects.filter(article=self)
    #

# class Tag(models.Model):
#     tag = models.CharField(max_length=50)
#     article = models.ForeignKey(Article)
#
#     class Meta:
#         verbose_name = _('Tag')
#         verbose_name_plural = _('Tags')
#         unique_together = (('tag', 'article'),)
#         index_together = [['tag', 'article'], ]
#
#     def __unicode__(self):
#         return self.tag
#
#     @staticmethod
#     def get_popular_tags():
#         tags = Tag.objects.all()
#         count = {}
#         for tag in tags:
#             if tag.article.status == Article.PUBLISHED:
#                 if tag.tag in count:
#                     count[tag.tag] = count[tag.tag] + 1
#                 else:
#                     count[tag.tag] = 1
#         sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
#         return sorted_count[:20]
#
#
# class ArticleComment(models.Model):
#     article = models.ForeignKey(Article)
#     comment = models.CharField(max_length=500)
#     date = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User)
#
#     class Meta:
#         verbose_name = _("Article Comment")
#         verbose_name_plural = _("Article Comments")
#         ordering = ("date",)
#
#     def __unicode__(self):
#         return u'{0} - {1}'.format(self.user.username, self.article.title)

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template import Template, TemplateSyntaxError, TemplateDoesNotExist, Context
from django.template.loader import get_template
from django.core.exceptions import ValidationError


def validate_template_syntax(source):
    """
    Basic Django Template syntax validation. This allows for robuster template
    authoring.
    """
    try:
        Template(source)
    except (TemplateSyntaxError, TemplateDoesNotExist) as err:
        raise ValidationError(str(err))


class EmailTemplate(models.Model):
    class Meta:
        verbose_name = _("Email Template")
        verbose_name_plural = _("Email Templates")

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    subject = models.CharField(
        max_length=255, null=False, blank=False, validators=[validate_template_syntax]
    )
    from_email = models.EmailField(
        null=True,
        blank=True,
        help_text="If not set, default mail will be used.",
    )
    plain_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Plain text content",
        help_text="If template field is set, this message will be ignored",
        default="Hi {{ user }}, Maktabiya, A Desk Booking App!",
    )
    html_template = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Custom template to use for the email. (Paths relative to \
            `settings.TEMPLATES[i]['DIRS']`)",
        default=None,
        validators=[validate_template_syntax],
    )
    active = models.BooleanField(default=True)

    def get_sender(self):
        if hasattr(self, "from_email") and self.from_email:
            return self.from_email

    def render_html_text(self, context):
        template = get_template(
            self.html_template
        )  # Adjust the template path as per your project structure
        html_message = template.render(context)
        return html_message

    def render_subject(self, context):
        template = Template(self.subject)
        return template.render(Context(context))

    def render_plain_message(self, context):
        template = Template(self.plain_message)
        return template.render(Context(context))

    def __str__(self):
        return self.name

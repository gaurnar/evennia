"""
Various helpers for I18N.

"""

from django.conf import settings


def translated_list(translated, strip=True):
    """ Use with _() to handle translated lists (e.g. command aliases) """
    if not translated.strip():
        # could be no viable aliases for some languages
        return []
    return [alias.strip() if strip else alias for alias in translated.split(",")]


def send_action_message(subject, objects, subject_message, third_person_message, conj_message):
    """ Send action message considering NO_VERB_CONJUGATION setting. """
    obj_name = objects[0].get_numbered_name(len(objects), subject, return_string=True)
    if settings.NO_VERB_CONJUGATION:
        subj_name = subject.get_display_name() if hasattr(subject, "get_display_name") else str(subject)
        
        subject.msg(subject_message.format(obj_name=obj_name))

        subject.location.msg_contents(
            third_person_message.format(subj_name=subj_name, obj_name=obj_name),
            from_obj=subject,
            exclude=subject,
        )
    else:
        subject.location.msg_contents(
            conj_message.format(obj_name=obj_name),
            from_obj=subject,
        )

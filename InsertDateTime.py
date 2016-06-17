#
# Name:            InsertDateTime
#
# File:            InsertDateTime.py
#
# Requirements:    Plugin for Sublime Text v2 and v3
#
# Written by:      mattst - https://github.com/mattst
#
# ST Command:      insert_date_time
#
# Optional Arg:    format: a date time formatting string (see below) which
#                  controls which date time string should be inserted.
#
# Setting File:    InsertDateTime.sublime-settings
#
# Settings Fields: formats: a list of date time formatting strings (see below)
#                  which controls which date time strings will be displayed in
#                  the overlay panel for user selection.
#
#                  fixed_width_font: a boolean value which controls whether to
#                  use a fixed width font in the overlay panel (default: true)
#
# Formats:
#
# The date time formatting strings must be in the form used by the strftime()
# method of the Python DateTime class. For example "%Y-%m-%d" would give a date
# like "2016-06-17", while "%A %d %B %Y" would give "Friday 17 June 2016".
#
# Note that "%Z" (time zone name) and "%z" (UTC offset) can not be used as these
# rely of information unavailable to a plugin for Sublime Text. However the UTC
# offset value can be retrieved by other means and it will be shown by various
# timestamps listed below.
#
# Lists of Python date time formatting characters can be viewed here:
# http://docs.python.org/3.3/library/time.html#time.strftime
# http://docs.python.org/2.6/library/datetime.html#strftime-strptime-behavior
#
# In addition the following formatting strings may be used:
#
# timestamp_iso_8601:        A timestamp in the following form:
#                            2016-05-29T16:07:59+01:00
#                            Used by: ISO 8601 and RFC 3339
#                            This is the international and Internet standard.
#
# timestamp_rfc_3339:        Same as: timestamp_iso_8601
#                            ISO 8601, the international standard, was
#                            adapted from RFC 3339 the Internet standard.
#
# timestamp_rfc_3339_human:  A timestamp in the following form:
#                            2016-05-29 16:07:59+01:00
#                            Human readable form of: RFC 3339
#                            Not valid under ISO 8601.
#
# timestamp_rfc_5322:        A timestamp in the following form:
#                            Sun, 29 May 2016 16:07:59 +0100
#                            Used by: RFC 5321, 5322
#                            This is the standard used by email.
#
# timestamp_posix_time:      POSIX time, aka Unix or Epoch time; the
#                            total number of elapsed seconds since:
#                            1970-01-01 00:00:00 +00:00
#
# Usage:
#
# When the InsertDateTime plugin is run it first checks to see if the calling
# command used the optional "format" arg, if so the appropriate date time string
# will be inserted immediately. If the command was not run with the "format" arg
# then the plugin will display the overlay panel with the date time strings that
# correspond to those set in the "formats" list in the settings file. Note that
# the plugin works with multiple selections.
#
# Key Bindings Examples:
#
# Show the overlay panel with the date time strings:
#
# { "keys": ["ctrl+?"], "command": "insert_date_time" },
#
# Immediately insert the specified date time string:
#
# { "keys": ["ctrl+?"], "command": "insert_date_time",
#                       "args": {"format": "%Y-%m-%d"} },
#
# { "keys": ["ctrl+?"], "command": "insert_date_time",
#                       "args": {"format": "timestamp_iso_8601"} },
#
# InsertDateTime.sublime-settings File Example:
#
# {
#     "formats":
#     [
#         "%H:%M:%S",
#         "%Y-%m-%d",
#         "%Y-%m-%d %H:%M",
#         "%d-%m-%Y",
#         "%d %B %Y",
#         "%A %d %B %Y",
#         "timestamp_iso_8601",
#     ],
#     "fixed_width_font": true
# }
#

import sublime
import sublime_plugin
import time
from datetime import datetime

class InsertDateTimeCommand(sublime_plugin.TextCommand):
    """
    The InsertDateTimeCommand class is a Sublime Text plugin which inserts a
    date time string. The format for the date time string can be specified in
    the calling command's "format" arg, for immediate insertion, or in the
    "formats" list in the InsertDateTime.sublime-settings file, in which case a
    list of date time strings will be displayed for the user to select from in
    the overlay panel.
    """

    def run(self, edit, **kwargs):
        """ This is called when the command is run. """

        self.date_time = datetime.now()

        # Check if the plugin command was run with a valid "format" arg,
        # if so then insert the appropriate date time string and return.

        date_time_str = self.get_date_time_str_from_format_arg(**kwargs)

        if date_time_str is not None:
            self.insert_date_time_string(date_time_str)
            return

        # The plugin command was NOT run with the "format" arg so display
        # the date time strings in the overlay panel for user selection.

        self.display_date_time_strings_in_overlay()


    def get_date_time_str_from_format_arg(self, **kwargs):
        """
        Determines if the plugin was run with the "format" arg and, if so,
        returns the corresponding date time string, if not it returns None.
        """

        format_string = kwargs.get("format", None)

        if format_string is None:
            return None

        # get_date_time_str() returns None if format_string is invalid.

        return self.get_date_time_str(format_string)


    def insert_date_time_string(self, date_time_str):
        """ Inserts the date time string at the cursor point(s). """

        self.view.run_command('insert', {'characters': date_time_str})


    def display_date_time_strings_in_overlay(self):
        """
        Loads the format strings from the settings file and displays the
        corresponding date time strings in the overlay for user selection.
        """

        settings_file = "InsertDateTime.sublime-settings"
        settings = sublime.load_settings(settings_file)
        format_strings = settings.get("formats", [])
        fixed_width_font = settings.get("fixed_width_font", True)

        self.date_time_strings = []
        self.populate_date_time_strings(format_strings)

        # Nothing to display.
        if len(self.date_time_strings) == 0:
            msg = "Set the list of date time formats in: " + settings_file
            sublime.status_message(msg)
            return

        font_flag = sublime.MONOSPACE_FONT if fixed_width_font else 0

        self.view.window().show_quick_panel(self.date_time_strings,
                                self.on_overlay_selection_done, font_flag)


    def on_overlay_selection_done(self, selected_index):
        """ This is called with the selected index from the overlay. """

        # User cancelled the overlay.
        if selected_index == -1:
            return

        date_time_str = self.date_time_strings[selected_index]
        self.insert_date_time_string(date_time_str)


    def populate_date_time_strings(self, format_strings):
        """ Populates the date_time_strings list. """

        for format_string in format_strings:

            date_time_str = self.get_date_time_str(format_string)

            if date_time_str is not None:
                # Avoid duplicate entries.
                if date_time_str not in self.date_time_strings:
                    self.date_time_strings.append(date_time_str)


    def get_date_time_str(self, format_string):
        """ Returns the appropriate date time string or None. """

        if not self.is_format_str_valid(format_string):
            return None

        # The various date time strings provided directly by this plugin.

        if format_string == "timestamp_iso_8601":
            return self.get_timestamp_iso_8601()

        if format_string == "timestamp_rfc_3339":
            return self.get_timestamp_iso_8601()

        elif format_string == "timestamp_rfc_3339_human":
            return self.get_timestamp_rfc_3339_human()

        elif format_string == "timestamp_rfc_5322":
            return self.get_timestamp_rfc_5322()

        elif format_string == "timestamp_posix_time":
            return self.get_timestamp_posix_time()

        # Convert a Python date time format string.
        else:
            return self.date_time.strftime(format_string)


    def is_format_str_valid(self, format_string):
        """ Determines if format_string is valid for use. """

        # isinstance() needs a Python version dependant string
        # class; ST v3 uses Python 3.3, ST v2 uses Python 2.6.

        sublime_text_v3 = int(sublime.version()) >= 3000

        if sublime_text_v3:
            if not isinstance(format_string, str):
                return False
        else:
            if not isinstance(format_string, basestring):
                return False

        if len(format_string) == 0:
            return False

        return True


    def get_timestamp_iso_8601(self):
        """
        Returns a timestamp in the form: 2016-05-29T16:07:59+01:00
        This is the most common timestamp: ISO 8601 and RFC 3339.
        ISO 8601 is the international timestamp standard which was
        adapted from RFC 3339, the Internet timestamp standard.
        """

        format_style = "%Y-%m-%dT%H:%M:%S"
        date_time_str = self.date_time.strftime(format_style)
        date_time_str += self.get_utc_offset_str()
        return date_time_str


    def get_timestamp_rfc_3339_human(self):
        """
        Returns a timestamp in the form: 2016-05-29 16:07:59+01:00
        The widely used, more easily readable, form of: RFC 3339
        This variation is not allowed under ISO 8601.
        """

        return self.get_timestamp_iso_8601().replace("T", " ")


    def get_timestamp_rfc_5322(self):
        """
        Returns a timestamp in the form: Sun, 29 May 2016 16:07:59 +0100
        This is the standard form used in sending email: RFC 5321, 5322
        """

        format_style = "%a, %d %b %Y %H:%M:%S"
        date_time_str = self.date_time.strftime(format_style)
        date_time_str += " " + self.get_utc_offset_str().replace(":", "")
        return date_time_str


    def get_timestamp_posix_time(self):
        """
        Returns POSIX time, aka Unix time aka Epoch time; the number
        of seconds that have elapsed since 1970-01-01T00:00:00+00:00.
        """

        timestamp = time.time()
        time_posix = str(int(timestamp))
        return time_posix


    def get_utc_offset_str(self):
        """
        Returns a UTC offset string of the current time suitable for use in the
        most widely used timestamps (i.e. ISO 8601, RFC 3339). e.g. 10 hours
        ahead, 5 hours behind, and time is UTC: "+10:00", "-05:00", "+00:00".
        """

        # Note that total_seconds() is Python 2.7+ so can
        # not be used below because ST v2 uses Python 2.6.
        # See git revision "a26551d4b2" for the old code.

        timestamp = time.time()
        time_now = datetime.fromtimestamp(timestamp)
        time_utc = datetime.utcfromtimestamp(timestamp)

        if time_now >= time_utc:
            time_diff = time_now - time_utc
            utc_offset_prefix = "+"
        else:
            time_diff = time_utc - time_now
            utc_offset_prefix = "-"

        utc_offset = time.gmtime(time_diff.seconds)
        utc_offset_str = time.strftime("%H:%M", utc_offset)

        return utc_offset_prefix + utc_offset_str

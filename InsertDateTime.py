#
# Name:            InsertDateTime
#
# File:            InsertDateTime.py
#
# Requirements:    Plugin for Sublime Text v3
#
# Written by:      mattst - https://github.com/mattst
#
# ST Command:      insert_date_time
#
# Optional Arg:    format: a date time formatting string (see below)
#
# Setting File:    InsertDateTime.sublime-settings
#
# Settings Fields: formats: a list of date time formatting strings (see below)
#                  which controls which date time stamps will be displayed in
#                  the overlay panel for user selection.
#
#                  fixed_width_font: a boolean value which controls whether to
#                  use a fixed width font in the overlay panel (default: true)
#
# Formats:
#
# The date time formatting strings must be in the form used by the strftime()
# method of the Python DateTime class. For example "%Y-%m-%d" would give a date
# of "YYYY-MM-DD".
#
# Note that "%Z" (time zone name) and "%z" (UTC offset) can not be used as these
# rely of information unavailable to a plugin for Sublime Text. However the UTC
# offset value can be retrieved by other means and it will be shown by the
# timestamps listed below (with the exception of timestamp_posix_time).
#
# The list of formatting characters can be viewed here:
# http://docs.python.org/3.3/library/time.html#time.strftime
# http://docs.python.org/2.6/library/datetime.html#strftime-strptime-behavior
#
# In addition the following formatting strings may be used:
#
# timestamp_iso_8601:        a timestamp in the following form:
#                            2016-05-29T16:07:59+01:00
#                            Used by: ISO 8601 and RFC 3339
#                            This is the international standard.
#
# timestamp_rfc_3339:        same as: timestamp_iso_8601
#                            ISO 8601, the international standard, was
#                            adapted from RFC 3339 the Internet standard.
#
# timestamp_rfc_3339_human:  a timestamp in the following form:
#                            2016-05-29 16:07:59+01:00
#                            Human readable form of: RFC 3339
#                            Not valid under ISO 8601.
#
# timestamp_rfc_5322:        a timestamp in the following form:
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
# command used the optional "format" arg with a date time string, if so the
# appropriate date time stamp will be inserted immediately. If the command was
# not run with the "format" arg then it will display the overlay panel which
# will contain the date time stamps corresponding to those set in the "formats"
# list in the settings file. Note: the plugin works with multiple selections.
#
# Key Bindings Examples:
#
# Show the overlay panel with the date time stamps:
#
# { "keys": ["ctrl+?"], "command": "insert_date_time" },
#
# Immediately insert the specified date time stamps:
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
    date time stamp. The format for the date time stamp can be specified in the
    calling command's "format" arg, for immediate insertion, or in the "formats"
    list in the InsertDateTime.sublime-settings file, in which case a list of
    date time stamps will be displayed for user selection in the overlay panel.
    """

    def run(self, edit, **kwargs):
        """ This is called when the command is run. """

        self.date_time = datetime.now()

        # Check if the plugin command was run with the "format" arg.
        # If so insert the appropriate date time string and return.

        format_string = kwargs.get("format", None)

        if format_string is not None:
            date_time_str = self.get_date_time_str(format_string)

            if date_time_str is not None:
                self.insert_date_time_stamp(date_time_str)
                return

        # The plugin command was NOT run with the "format" arg so...
        # Load the format strings from the settings file and display
        # the date time strings in the overlay for user selection.

        settings_file = "InsertDateTime.sublime-settings"
        settings = sublime.load_settings(settings_file)
        format_strings = settings.get("formats", [])
        fixed_width_font = settings.get("fixed_width_font", True)

        self.date_time_stamps = []
        self.populate_date_time_stamps(format_strings)

        # Nothing to display.
        if len(self.date_time_stamps) == 0:
            msg = "Set the list of date time formats in: " + settings_file
            sublime.status_message(msg)
            return

        if fixed_width_font: font_flag = sublime.MONOSPACE_FONT
        else:                font_flag = 0

        self.view.window().show_quick_panel(self.date_time_stamps,
                                self.on_overlay_selection_done, font_flag)


    def on_overlay_selection_done(self, selected_index):
        """ This is called with the selected index from the overlay. """

        # User cancelled the overlay.
        if selected_index == -1:
            return

        date_time_str = self.date_time_stamps[selected_index]
        self.insert_date_time_stamp(date_time_str)


    def insert_date_time_stamp(self, date_time_str):
        """ Inserts the date time stamp at the cursor point(s). """

        self.view.run_command('insert', {'characters': date_time_str})


    def populate_date_time_stamps(self, format_strings):
        """ Populates the date_time_stamps list. """

        for format_string in format_strings:

            date_time_str = self.get_date_time_str(format_string)

            if date_time_str is not None:
                # Avoid duplicate entries.
                if date_time_str not in self.date_time_stamps:
                    self.date_time_stamps.append(date_time_str)


    def get_date_time_str(self, format_string):
        """ Returns the appropriate date time stamp string. """

        # Ignore empty strings or values which are not a string.

        try:
            if len(format_string) == 0:
                raise ValueError

        except Exception:
            return None

        # The various timestamps provided directly by this plugin.

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

        # Converts a Python date time format string.
        else:
            return self.date_time.strftime(format_string)


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
        most widely used timestamps (i.e. ISO 8601, RFC 3339). For example:
        10 hours ahead, 5 hours behind, and time is UTC: +10:00, -05:00, +00:00
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
        utc_offset_fmt = time.strftime("%H:%M", utc_offset)
        utc_offset_str = utc_offset_prefix + utc_offset_fmt

        return utc_offset_str

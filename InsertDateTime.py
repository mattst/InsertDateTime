#
# Name:            InsertDateTime
#
# File:            InsertDateTime.py
#
# Requirements:    Plugin for Sublime Text v.2 and v.3
#
# Tested:          ST v.3 build 3065 - tested and working.
#                  ST v.2 build 2221 - tested and working.
#
# Written by:      Matthew Stanfield
#
# Last Edited:     2015-02-02
#
# ST Command:      insert_date_time
#
# Optional Arg:    index: an integer value indexing into the date_time_stamps list. If used the
#                  required date time stamp will be inserted and the overlay panel will not be
#                  shown for the user to select a date time stamp from.
#
# Description:     See class description below.
#


import sublime
import sublime_plugin
import datetime


class InsertDateTimeCommand(sublime_plugin.TextCommand):
    """
    The InsertDateTimeCommand class is a Sublime Text plugin which inserts a variety of date time
    stamps either by the user specifying one in the command's args or by selecting one from a list
    displayed in the overlay panel.
    """


    def run(self, edit, **kwargs):
        """
        run() is called when the command is run.
        """

        # Storage for the various date time stamps.
        self.date_time_stamps = []

        # Populate the date_time_stamps list.
        self.populate_date_time_stamps()

        # The desired date time stamp can be set either by the use of the 'index' command arg or
        # by selecting from a list displayed in the overlay panel.

        # If the 'index' arg was used set the index into the date_time_stamps list.
        # Note: get_index_setting() will return None if 'index' was not used/invalid.
        date_time_stamp_index = self.get_index_setting(**kwargs)

        # The 'index' arg was used to set the index into the date_time_stamps list.
        if date_time_stamp_index is not None:

            # Insert the chosen date time stamp.
            self.insert_date_time_stamp(date_time_stamp_index)

        # The 'index' arg was not used.
        else:

            # Show the overlay with the date time stamps for user selection.
            self.view.window().show_quick_panel(self.date_time_stamps, self.on_select)

    # End of def run()


    def get_index_setting(self, **kwargs):
        """
        get_index_setting() returns the value of the 'index' arg in the kwargs dictionary if it
        exists, and it is an integer in the correct range, otherwise it returns None.
        """

        # If available get the 'index' arg from the kwargs dictionary.
        if 'index' in kwargs:
            index_arg_val = kwargs.get('index')
        else:
            return None

        # Check that index_arg_val is an integer and in range to index the date_time_stamps list.

        date_time_stamps_upper_bound = len(self.date_time_stamps) - 1

        # A warning message to display if the 'index' arg is invalid.
        msg = "insert_date_time command: 'index' arg is not an integer in the range 0 to {0:d}"
        msg = msg.format(date_time_stamps_upper_bound)

        # Note: isinstance(x, int) returns true if x is a bool, so check it is not a bool.
        if ( not isinstance(index_arg_val, int) or isinstance(index_arg_val, bool) or
             index_arg_val < 0 or index_arg_val > date_time_stamps_upper_bound ):

            # Output the warning message to the status bar.
            sublime.status_message(msg)
            return None

        # The 'index' arg is in the kwargs dictionary and is set correctly.
        return index_arg_val

    # End of def get_index_setting()


    def on_select(self, selected_index):
        """
        on_select() will be called with the selected index from the overlay.
        """

        # No selection was made, the overlay was cancelled.
        if selected_index == -1:
            return

        # Insert the chosen date time stamp.
        self.insert_date_time_stamp(selected_index)

    # End of def on_select()


    def insert_date_time_stamp(self, selected_index):
        """
        insert_date_time_stamp() inserts the date time stamp at the cursor point(s).
        """

        # Get the text of the selected date time stamp.
        date_time_str = self.date_time_stamps[selected_index]

        # Insert the chosen date time stamp at the cursor point(s).
        self.view.run_command('insert', {'characters': date_time_str})

    # End of def insert_date_time_stamp()


    def populate_date_time_stamps(self):
        """
        populate_date_time_stamps() fills the date_time_stamps list.
        """

        # Get the current date and time.
        date_time = datetime.datetime.now()

        # The format codes can be viewed in section 8.1.7 of the url below:
        # https://docs.python.org/2/library/datetime.html

        # The order added below will be the same as displayed in the overlay.

        # ToDo: Before distribution add US date formats. e.g. 10/19/2014

        # e.g. Sun 19 Oct 2014
        date_time_str = date_time.strftime('%a %d %b %Y')
        self.date_time_stamps.append(date_time_str)

        # e.g. Sun 19th Oct 2014
        ord_num_abbrv = self.get_ordinal_num_abbrv(date_time.day)
        date_time_str =  date_time.strftime('%a %d') + ord_num_abbrv
        date_time_str += date_time.strftime(' %b %Y')
        self.date_time_stamps.append(date_time_str)

        # e.g. Sun 19 Oct 2014 16:28
        date_time_str = date_time.strftime('%a %d %b %Y %H:%M')
        self.date_time_stamps.append(date_time_str)

        # e.g. Sunday 19 October 2014
        date_time_str = date_time.strftime('%A %d %B %Y')
        self.date_time_stamps.append(date_time_str)

        # e.g. Sunday 19th October 2014
        ord_num_abbrv = self.get_ordinal_num_abbrv(date_time.day)
        date_time_str =  date_time.strftime('%A %d') + ord_num_abbrv
        date_time_str += date_time.strftime(' %B %Y')
        self.date_time_stamps.append(date_time_str)

        # e.g. 19 Oct 2014
        date_time_str = date_time.strftime('%d %b %Y')
        self.date_time_stamps.append(date_time_str)

        # e.g. 19 October 2014
        date_time_str = date_time.strftime('%d %B %Y')
        self.date_time_stamps.append(date_time_str)

        # e.g. 19-10-2014
        date_time_str = date_time.strftime('%d-%m-%Y')
        self.date_time_stamps.append(date_time_str)

        # e.g. 19/10/2014
        date_time_str = date_time.strftime('%d/%m/%Y')
        self.date_time_stamps.append(date_time_str)

        # e.g. 2014-10-19
        date_time_str = date_time.strftime('%Y-%m-%d')
        self.date_time_stamps.append(date_time_str)

        # e.g. 2014-10-19 16:28
        date_time_str = date_time.strftime('%Y-%m-%d %H:%M')
        self.date_time_stamps.append(date_time_str)

        # e.g. 2014-10-19 16:28:57
        date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.date_time_stamps.append(date_time_str)

        # e.g. 2014-10-19T16:28:57
        date_time_str = date_time.strftime('%Y-%m-%dT%H:%M:%S')
        self.date_time_stamps.append(date_time_str)

    # End of def populate_date_time_stamps()


    def get_ordinal_num_abbrv(self, day_of_month):
        """
        get_ordinal_num_abbrv() returns a string containing the ordinal number abbreviation of the
        day_of_month argument. Ordinal numbers are first, second, third, etc. Ordinal number
        abbreviations are the suffix added to an integer to turn that integer into an ordinal
        number, for example the 'st' part of '1st', the 'nd' of '2nd', and so on.
        """

        if day_of_month == 1 or day_of_month == 21 or day_of_month == 31:
            return "st"

        elif day_of_month == 2 or day_of_month == 22:
            return "nd"

        elif day_of_month == 3 or day_of_month == 23:
            return "rd"

        else:
            return "th"

    # End of def get_ordinal_num_abbrv()

# End of InsertDateTimeCommand() class.

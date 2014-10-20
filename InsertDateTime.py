#
# Name:             InsertDateTime
#
# File:             InsertDateTime.py
#
# Requirements:     Plugin for Sublime Text v.2 and v.3
#
# Tested:           ST v.3 build 3065 - tested and working.
#                   ST v.2 build 2221 - tested and working.
#
# Written by:       mattst - https://github.com/mattst
#
# Url:              n/a
#
# Version:          n/a
#
# ST Command:       insert_date_time
#
# Description:      See class description below.
#

import sublime
import sublime_plugin
import datetime

class InsertDateTimeCommand(sublime_plugin.TextCommand):
    """
    The InsertDateTimeCommand class is a Sublime Text plugin which creates an
    overlay panel with a variety of date and/or time stamps and inserts the
    chosen one into the file at the cursor point(s).
    """


    def run(self, edit):
        """
        run() is called when the command is run. Duhhh. :)
        """

        # Storage for the various date and/or time stamps.
        self.date_time_stamps = []

        # Populate the date_time_stamps list.
        self.populate_date_time_stamps()

        # Show the overlay with the date and/or time stamps. Set it to call the
        # on_select() method with the index of the selected item.
        self.view.window().show_quick_panel(self.date_time_stamps,
                                                self.on_select)

    # End of def run()


    def on_select(self, selected_index):
        """
        on_select() will be called with the selected index from the overlay.
        """

        # No selection made, overlay was cancelled.
        if selected_index == -1:
            return

        # Get the chosen date and/or time stamp.
        date_str = self.date_time_stamps[selected_index]

        # Note that view.insert() can not be used for the text insertion below
        # because it requires the 'edit' object which will have expired when
        # run() returned just before this method was called. Edit objects are
        # not user creatable in ST v3 (although they are in v2), see the APIs.

        # Insert the chosen date and/or time stamp at the cursor point(s).
        self.view.run_command('insert', {'characters': date_str})

    # End of def on_select()


    def populate_date_time_stamps(self):
        """
        populate_date_time_stamps() fills the date_time_stamps list.
        """

        # Store the current date and time.
        date_time = datetime.datetime.now()

        # The format codes can be viewed in section 8.1.7 of the url below:
        # https://docs.python.org/2/library/datetime.html

        # The order added below will be the same as displayed in the overlay.

        # e.g. Sun 19 Oct 2014
        date_str = date_time.strftime('%a %d %b %Y')
        self.date_time_stamps.append(date_str)

        # e.g. Sun 19th Oct 2014
        ord_num_abbrv = self.get_ordinal_num_abbrv(date_time.day)
        date_str = (date_time.strftime('%a %d') + ord_num_abbrv +
                                        date_time.strftime(' %b %Y'))
        self.date_time_stamps.append(date_str)

        # e.g. Sun 19 Oct 2014 16:28
        date_str = date_time.strftime('%a %d %b %Y %H:%M')
        self.date_time_stamps.append(date_str)

        # e.g. Sunday 19 October 2014
        date_str = date_time.strftime('%A %d %B %Y')
        self.date_time_stamps.append(date_str)

        # e.g. Sunday 19th October 2014
        ord_num_abbrv = self.get_ordinal_num_abbrv(date_time.day)
        date_str = (date_time.strftime('%A %d') + ord_num_abbrv +
                                        date_time.strftime(' %B %Y'))
        self.date_time_stamps.append(date_str)

        # e.g. 19 Oct 2014
        date_str = date_time.strftime('%d %b %Y')
        self.date_time_stamps.append(date_str)

        # e.g. 19 October 2014
        date_str = date_time.strftime('%d %B %Y')
        self.date_time_stamps.append(date_str)

        # e.g. 2014-10-19
        date_str = date_time.strftime('%Y-%m-%d')
        self.date_time_stamps.append(date_str)

        # e.g. 2014-10-19 16:28
        date_str = date_time.strftime('%Y-%m-%d %H:%M')
        self.date_time_stamps.append(date_str)

        # e.g. 2014-10-19 16:28:57
        date_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.date_time_stamps.append(date_str)

        # e.g. 2014-10-19T16:28:57
        date_str = date_time.strftime('%Y-%m-%dT%H:%M:%S')
        self.date_time_stamps.append(date_str)

        # e.g. 19-10-2014
        date_str = date_time.strftime('%d-%m-%Y')
        self.date_time_stamps.append(date_str)

        # e.g. 19/10/2014
        date_str = date_time.strftime('%d/%m/%Y')
        self.date_time_stamps.append(date_str)

    # End of def populate_date_time_stamps()


    def get_ordinal_num_abbrv(self, day_of_month):
        """
        get_ordinal_num_abbrv() returns a string containing the ordinal number
        abbreviation of the day_of_month argument. e.g. 1st, 2nd, 3rd, 4th.
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

### InsertDateTime - A Plugin for Sublime Text v2 and v3

A Sublime Text plugin to insert date time stamps.

### Installation:

Manual installation only, this plugin has not been submitted to Package Control.

### In Brief:

    ST Command:      insert_date_time

    Optional Arg:    format: a date time formatting string (see below) which
                     controls which date time string should be inserted.

    Settings File:   InsertDateTime.sublime-settings

    Settings Fields:
                     formats: a list of date time formatting strings (see below)
                     which controls which date time strings will be displayed in
                     the overlay panel for user selection.

                     fixed_width_font: a boolean value which controls whether to
                     use a fixed width font in the overlay panel (default: true)

### Formats:

The date time formatting strings must be in the form used by the `strftime()` method of the Python DateTime class. For example `"%Y-%m-%d"` would give a date like `2016-06-17`, while `"%A %d %B %Y"` would give `Friday 17 June 2016`.

Lists of Python date time formatting characters can be viewed here: [Python.org strftime()](http://docs.python.org/3.3/library/time.html#time.strftime)

Note that `%Z` (time zone name) and `%z` (UTC offset) can not be used as these rely of information unavailable to a Sublime Text plugin. However the UTC offset value can be shown by the various standardized timestamps listed below.

The following standardized formatting strings may be used as the `format` arg or in the `formats` settings list:

    timestamp_iso_8601:        A timestamp in the following form:
                               2016-05-29T16:07:59+01:00
                               Used by: ISO 8601 and RFC 3339
                               This is the international and Internet standard.

    timestamp_rfc_3339:        Same as: timestamp_iso_8601
                               ISO 8601, the international standard, was
                               adapted from RFC 3339 the Internet standard.

    timestamp_rfc_3339_human:  A timestamp in the following form:
                               2016-05-29 16:07:59+01:00
                               Human readable form of: RFC 3339
                               Not valid under ISO 8601.

    timestamp_rfc_5322:        A timestamp in the following form:
                               Sun, 29 May 2016 16:07:59 +0100
                               Used by: RFC 5321, 5322
                               This is the standard used by email.

    timestamp_posix_time:      POSIX time, aka Unix or Epoch time; the
                               total number of elapsed seconds since:
                               1970-01-01 00:00:00 +00:00

### Usage:

The plugin can be launched by selecting `Insert Date Time` from the `Command Palette` or from key bindings that users must manually add by placing key bindings in their `Default (OS Name).sublime-keymap` file.

When the `InsertDateTime` plugin is run it first checks to see if the calling command included the optional `format` arg, if so the appropriate date time string will be inserted immediately.

If the command was not run with the `format` arg then the plugin will display the overlay panel with the date time strings that correspond to those set in the `formats` list in the settings file.

Note that the plugin works with multiple selections.

### Key Bindings Examples:

    Show the overlay panel with all the date time strings:
    { "keys": ["ctrl+?"], "command": "insert_date_time" },

    Insert the specified date time string:
    { "keys": ["ctrl+?"], "command": "insert_date_time", "args": {"format": "%Y-%m-%d"} },

    Insert the timestamp_iso_8601 date time string:
    { "keys": ["ctrl+?"], "command": "insert_date_time", "args": {"format": "timestamp_iso_8601"} },

### InsertDateTime.sublime-settings Example:

The default `InsertDateTime.sublime-settings` has 15 different date time stamps, users can overwrite this with their own file by placing a file called `InsertDateTime.sublime-settings` in their ST `User` config folder.

Users can view the default, and edit their user file, by clicking on the preferences menu:

    ST Menu --> Preferences --> Package Settings --> InsertDateTime

Here is an example `InsertDateTime.sublime-settings` file:

    {
        "formats":
        [
            "%H:%M:%S",
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y",
            "%d %B %Y",
            "%A %d %B %Y",
            "timestamp_iso_8601",
        ],
        "fixed_width_font": true
    }

### License

This package is licensed under The MIT License (MIT).

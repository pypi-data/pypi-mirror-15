confset
*******

.. image:: https://travis-ci.org/dwighthubbard/confset.svg?branch=master
    :target: https://travis-ci.org/dwighthubbard/confset

Set and view values for package default settings from the command line.

Installing confset
==================

Confset is a normal python package and can be installed using pip.

.. code-block::

    pip install confset

Using confset from the command line
===================================

Here are some simple examples of using the confset command from the
command line.

Showing all settings
~~~~~~~~~~~~~~~~~~~~

Running confset without arguments will show all configuration
settings on the system.

.. code-block::

    $ confset
    console-setup.VERBOSE_OUTPUT="no"
    console-setup.ACTIVE_CONSOLES="/dev/tty[1-6]"
    console-setup.CHARMAP="UTF-8"
    console-setup.CODESET="Uni2"
    console-setup.FONTFACE="Fixed"
    console-setup.FONTSIZE="16"
    devpts.TTYGRP=5
    devpts.TTYMODE=620
    halt.HALT=poweroff
    keyboard.XKBMODEL="pc105"
    keyboard.XKBLAYOUT="us"
    keyboard.XKBVARIANT=""
    keyboard.XKBOPTIONS=""
    nss.ADJUNCT_AS_SHADOW=TRUE
    ntpdate.NTPDATE_USE_NTP_CONF=yes
    ntpdate.NTPSERVERS="ntp.ubuntu.com"
    ntpdate.NTPOPTIONS=""
    rcS.UTC=yes
    rsyslog.RSYSLOGD_OPTIONS=""
    useradd.SHELL=/bin/sh
    $


Showing settings and any help comments associated with them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The --info flag tells confset to show the settings along with
any comment or help text associated with the setting in the
configuration file.

.. code-block::

    $ confset --info
    console-setup.VERBOSE_OUTPUT="no"             - Change to "yes" and setupcon will explain what is being doing
    console-setup.ACTIVE_CONSOLES="/dev/tty[1-6]" - Setup these consoles.  Most people do not need to change this.
    console-setup.CHARMAP="UTF-8"                 - Put here your encoding.  Valid charmaps are: UTF-8 ARMSCII-8 CP1251
                                                    CP1255 CP1256 GEORGIAN-ACADEMY GEORGIAN-PS IBM1133 ISIRI-3342
                                                    ISO-8859-1 ISO-8859-2 ISO-8859-3 ISO-8859-4 ISO-8859-5 ISO-8859-6
                                                    ISO-8859-7 ISO-8859-8 ISO-8859-9 ISO-8859-10 ISO-8859-11 ISO-8859-13
                                                    ISO-8859-14 ISO-8859-15 ISO-8859-16 KOI8-R KOI8-U TIS-620 VISCII
    console-setup.CODESET="Uni2"                  - The codeset determines which symbols are supported by the font.
                                                    Valid codesets are: Arabic Armenian CyrAsia CyrKoi CyrSlav Ethiopian
                                                    Georgian Greek Hebrew Lao Lat15 Lat2 Lat38 Lat7 Thai Uni1 Uni2 Uni3
                                                    Vietnamese.  Read README.fonts for explanation.
    console-setup.FONTFACE="Fixed"                - Valid font faces are: VGA (sizes 8, 14 and 16), Terminus (sizes
                                                    12x6, 14, 16, 20x10, 24x12, 28x14 and 32x16), TerminusBold (sizes
                                                    14, 16, 20x10, 24x12, 28x14 and 32x16), TerminusBoldVGA (sizes 14
                                                    and 16) and Fixed (sizes 13, 14, 15, 16 and 18).  Only when
                                                    CODESET=Ethiopian: Goha (sizes 12, 14 and 16) and
                                                    GohaClassic (sizes 12, 14 and 16).
                                                    Set FONTFACE and FONTSIZE to empty strings if you want setupcon to
                                                    set up the keyboard but to leave the console font unchanged.
    console-setup.FONTSIZE="16"
    devpts.TTYGRP=5                               - GID of the `tty' group
    devpts.TTYMODE=620                            - Set to 600 to have `mesg n' be the default
    halt.HALT=poweroff                            - Default behaviour of shutdown -h / halt. Set to "halt" or "poweroff".
    keyboard.XKBMODEL="pc105"
    keyboard.XKBLAYOUT="us"
    keyboard.XKBVARIANT=""
    keyboard.XKBOPTIONS=""
    nss.ADJUNCT_AS_SHADOW=TRUE                    - /etc/default/nss
                                                    This file can theoretically contain a bunch of customization variables
                                                    for Name Service Switch in the GNU C library.  For now there are only
                                                    four variables:
                                                    NETID_AUTHORITATIVE
                                                    If set to TRUE, the initgroups() function will accept the information
                                                    from the netid.byname NIS map as authoritative.  This can speed up the
                                                    function significantly if the group.byname map is large.  The content
                                                    of the netid.byname map is used AS IS.  The system administrator has
                                                    to make sure it is correctly generated.
                                                    NETID_AUTHORITATIVE=TRUE
                                                    SERVICES_AUTHORITATIVE
                                                    If set to TRUE, the getservbyname{,_r}() function will assume
                                                    services.byservicename NIS map exists and is authoritative, particularly
                                                    that it contains both keys with /proto and without /proto for both
                                                    primary service names and service aliases.  The system administrator
                                                    has to make sure it is correctly generated.
                                                    SERVICES_AUTHORITATIVE=TRUE
                                                    SETENT_BATCH_READ
                                                    If set to TRUE, various setXXent() functions will read the entire
                                                    database at once and then hand out the requests one by one from
                                                    memory with every getXXent() call.  Otherwise each getXXent() call
                                                    might result into a network communication with the server to get
                                                    the next entry.
                                                    SETENT_BATCH_READ=TRUE
                                                    ADJUNCT_AS_SHADOW
                                                    If set to TRUE, the passwd routines in the NIS NSS module will not
                                                    use the passwd.adjunct.byname tables to fill in the password data
                                                    in the passwd structure.  This is a security problem if the NIS
                                                    server cannot be trusted to send the passwd.adjuct table only to
                                                    privileged clients.  Instead the passwd.adjunct.byname table is
                                                    used to synthesize the shadow.byname table if it does not exist.
    ntpdate.NTPDATE_USE_NTP_CONF=yes              - Set to "yes" to take the server list from /etc/ntp.conf, from package ntp,
                                                    so you only have to keep it in one place.
    ntpdate.NTPSERVERS="ntp.ubuntu.com"           - List of NTP servers to use  (Separate multiple servers with spaces.)
                                                    Not used if NTPDATE_USE_NTP_CONF is yes.
    ntpdate.NTPOPTIONS=""                         - Additional options to pass to ntpdate
    rcS.UTC=yes                                   - assume that the BIOS clock is set to UTC time (recommended)
    rsyslog.RSYSLOGD_OPTIONS=""                   - Options for rsyslogd
                                                    -x disables DNS lookups for remote messages
                                                    See rsyslogd(8) for more details
    useradd.SHELL=/bin/sh                         - Default values for useradd(8)
                                                    The SHELL variable specifies the default login shell on your
                                                    system.
                                                    Similar to DHSELL in adduser. However, we use "sh" here because
                                                    useradd is a low level utility and should be as general
                                                    as possible
    $

See the settings and current values for the rsyslog daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's an example of modifying the rsyslog daemon configuration file.  On
Ubuntu this configuration is stored in the file /etc/default/rsyslog.  The
default configuration file looks like this:

.. code-block::

    # Options for rsyslogd
    # -x disables DNS lookups for remote messages
    # See rsyslogd(8) for more details
    RSYSLOGD_OPTIONS=""


We can see by looking at the file above it only has a single configuration
setting (RSYSLOGD_OPTIONS).  We can display the settings from this file
using confset like this:


.. code-block::

    $ confset --info rsyslog
    rsyslog.RSYSLOGD_OPTIONS="" - Options for rsyslogd
                                  -x disables DNS lookups for remote messages
                                  See rsyslogd(8) for more details
    $


To disable DNS lookups, using confset we would run the following command:


.. code-block::

    $ confset rsyslog.RSYSLOGD_OPTIONS='"-x"'
    $


Now if we look at the configuration file the setting is at the new value.


.. code-block::

    $ confset --info rsyslog
    rsyslog.RSYSLOGD_OPTIONS="-x"   - Options for rsyslogd
                                    -x disables DNS lookups for remote messages
                                    See rsyslogd(8) for more details
    $ cat /etc/default/rsyslog
    # Options for rsyslogd
    # -x disables DNS lookups for remote messages
    # See rsyslogd(8) for more details
    RSYSLOGD_OPTIONS="-x"
    $


Using confset from python
=========================

Here are some simple examples of using the confset python module.


Getting all system settings as a dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The confset settings function can be used to access all system settings
as a dictionary.

.. code-block:: python

    >>> import confset
    >>> confset.settings()
    {'nss.ADJUNCT_AS_SHADOW': {'help': ['/etc/default/nss', 'This file can theoretically contain a bunch of customization variables', 'for Name Service Switch in the GNU C library.  For now there are only', 'four variables:', 'NETID_AUTHORITATIVE', 'If set to TRUE, the initgroups() function will accept the information', 'from the netid.byname NIS map as authoritative.  This can speed up the', 'function significantly if the group.byname map is large.  The content', 'of the netid.byname map is used AS IS.  The system administrator has', 'to make sure it is correctly generated.', 'NETID_AUTHORITATIVE=TRUE', 'SERVICES_AUTHORITATIVE', 'If set to TRUE, the getservbyname{,_r}() function will assume', 'services.byservicename NIS map exists and is authoritative, particularly', 'that it contains both keys with /proto and without /proto for both', 'primary service names and service aliases.  The system administrator', 'has to make sure it is correctly generated.', 'SERVICES_AUTHORITATIVE=TRUE', 'SETENT_BATCH_READ', 'If set to TRUE, various setXXent() functions will read the entire', 'database at once and then hand out the requests one by one from', 'memory with every getXXent() call.  Otherwise each getXXent() call', 'might result into a network communication with the server to get', 'the next entry.', 'SETENT_BATCH_READ=TRUE', 'ADJUNCT_AS_SHADOW', 'If set to TRUE, the passwd routines in the NIS NSS module will not', 'use the passwd.adjunct.byname tables to fill in the password data', 'in the passwd structure.  This is a security problem if the NIS', 'server cannot be trusted to send the passwd.adjuct table only to', 'privileged clients.  Instead the passwd.adjunct.byname table is', 'used to synthesize the shadow.byname table if it does not exist.'], 'value': 'TRUE'}, 'keyboard.XKBOPTIONS': {'help': [], 'value': '""'}, 'devpts.TTYGRP': {'help': ["GID of the `tty' group"], 'value': '5'}, 'keyboard.XKBVARIANT': {'help': [], 'value': '""'}, 'console-setup.ACTIVE_CONSOLES': {'help': ['Setup these consoles.  Most people do not need to change this.'], 'value': '"/dev/tty[1-6]"'}, 'keyboard.XKBMODEL': {'help': [], 'value': '"pc105"'}, 'ntpdate.NTPOPTIONS': {'help': ['Additional options to pass to ntpdate'], 'value': '""'}, 'console-setup.FONTSIZE': {'help': [], 'value': '"16"'}, 'console-setup.CODESET': {'help': ['The codeset determines which symbols are supported by the font.', 'Valid codesets are: Arabic Armenian CyrAsia CyrKoi CyrSlav Ethiopian', 'Georgian Greek Hebrew Lao Lat15 Lat2 Lat38 Lat7 Thai Uni1 Uni2 Uni3', 'Vietnamese.  Read README.fonts for explanation.'], 'value': '"Uni2"'}, 'useradd.SHELL': {'help': ['Default values for useradd(8)', 'The SHELL variable specifies the default login shell on your', 'system.', 'Similar to DHSELL in adduser. However, we use "sh" here because', 'useradd is a low level utility and should be as general', 'as possible'], 'value': '/bin/sh'}, 'ntpdate.NTPSERVERS': {'help': ['List of NTP servers to use  (Separate multiple servers with spaces.)', 'Not used if NTPDATE_USE_NTP_CONF is yes.'], 'value': '"ntp.ubuntu.com"'}, 'console-setup.CHARMAP': {'help': ['Put here your encoding.  Valid charmaps are: UTF-8 ARMSCII-8 CP1251', 'CP1255 CP1256 GEORGIAN-ACADEMY GEORGIAN-PS IBM1133 ISIRI-3342', 'ISO-8859-1 ISO-8859-2 ISO-8859-3 ISO-8859-4 ISO-8859-5 ISO-8859-6', 'ISO-8859-7 ISO-8859-8 ISO-8859-9 ISO-8859-10 ISO-8859-11 ISO-8859-13', 'ISO-8859-14 ISO-8859-15 ISO-8859-16 KOI8-R KOI8-U TIS-620 VISCII'], 'value': '"UTF-8"'}, 'rsyslog.RSYSLOGD_OPTIONS': {'help': ['Options for rsyslogd', '-x disables DNS lookups for remote messages', 'See rsyslogd(8) for more details'], 'value': '"-x"'}, 'console-setup.VERBOSE_OUTPUT': {'help': ['Change to "yes" and setupcon will explain what is being doing'], 'value': '"no"'}, 'keyboard.XKBLAYOUT': {'help': [], 'value': '"us"'}, 'rcS.UTC': {'help': ['assume that the BIOS clock is set to UTC time (recommended)'], 'value': 'yes'}, 'devpts.TTYMODE': {'help': ["Set to 600 to have `mesg n' be the default"], 'value': '620'}, 'console-setup.FONTFACE': {'help': ['Valid font faces are: VGA (sizes 8, 14 and 16), Terminus (sizes', '12x6, 14, 16, 20x10, 24x12, 28x14 and 32x16), TerminusBold (sizes', '14, 16, 20x10, 24x12, 28x14 and 32x16), TerminusBoldVGA (sizes 14', 'and 16) and Fixed (sizes 13, 14, 15, 16 and 18).  Only when', 'CODESET=Ethiopian: Goha (sizes 12, 14 and 16) and', 'GohaClassic (sizes 12, 14 and 16).', 'Set FONTFACE and FONTSIZE to empty strings if you want setupcon to', 'set up the keyboard but to leave the console font unchanged.'], 'value': '"Fixed"'}, 'ntpdate.NTPDATE_USE_NTP_CONF': {'help': ['Set to "yes" to take the server list from /etc/ntp.conf, from package ntp,', 'so you only have to keep it in one place.'], 'value': 'yes'}, 'halt.HALT': {'help': ['Default behaviour of shutdown -h / halt. Set to "halt" or "poweroff".'], 'value': 'poweroff'}}
    >>>

Changing the ryslog RSYSLOGD_OPTIONS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's a simple example of changing a configuration setting using python.

.. code-block:: python

    >>> rsyslog_settings = confset.ConfigSettings('rsyslog')
    >>> rsyslog_settings.set('RSYSLOGD_OPTIONS', '"-x"')
    >>> rsyslog_settings.print_settings()
    rsyslog.RSYSLOGD_OPTIONS="-x"
    >>>


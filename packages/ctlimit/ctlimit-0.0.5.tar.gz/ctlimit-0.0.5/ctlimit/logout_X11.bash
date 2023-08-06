#!/bin/bash
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Esther Kruis and Anselm Kruis
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#


# expected arguments
# $1: user
# $2: X11 Display
# $3: warn seconds 1
# $4: warn seconds 2

# exec >>/tmp/.timeout.log 2>&1
printf '%s\n' "$0($$): $*" 1>&2

# aquire our own process group
# This is a little bit black magic, but we use perl to exec ourself with a
# new process group.
pgid=$$
[ $pgid -eq $(ps -p $pgid -o pgid=) ] || \
  exec perl -e 'setpgrp; exec{$ARGV[0]}@ARGV;die "$ARGV[0]: $!"' "$0" "$@"

# Now start the watchdog. It kills the process group as soon as STDIN gets closed.

# Magic: we dup stdin (fd0) to fd3, because fd0 becomes /dev/null for a background
# job.
exec 3<&0
( exec 0<&3 3<&- ; cd / ; dd ; trap "" TERM; kill -TERM -${pgid} ; : ) 2>/dev/null 1>&2 &
wdpid=$! ; exec 0< /dev/null 3<&- # change our stdin to /dev/null and getrid of fd3

# Now do the real work
# set -x
self="$0"
dir="$(dirname "$self")"
bdir=$dir/sudo_allowed
user="$1"
x11="$2"
typeset -i warn1="$3"
typeset -i warn2="$4"

typeset -i 'left=warn1 + warn2'

# commands
dbus_send=$(command -v dbus-send)
notify_send=$(command -v notify-send)
play=$(command -v play)
bin_kill=$(type -Pf kill)
killall=$(command -v killall)
xwininfo=$(command -v xwininfo)
xkill=$(command -v xkill)

if [ "$(id -u)" = "0" ] ; then
   env="$(command -v env)"
   cat="$(command -v cat)"
else
   env="$bdir/env"
   cat="$bdir/cat"
fi

# universal method to locate a session manager '*.SessionManager' with a Logout() method
test_dbus_universal() {
    typeset a="$1" ; shift
    sm_dest="$(sudo -n -u "$user" "$env" DBUS_SESSION_BUS_ADDRESS="$a" "$dbus_send" --session \
        --dest=org.freedesktop.DBus --type=method_call --print-reply --reply-timeout=20000 / org.freedesktop.DBus.ListNames | \
        sed -n -e 's/^ *string "\([^"]*\.SessionManager\)".*$/\1/p')"
    if [ -n "$sm_dest" ] ; then
        sm_pid="$(sudo -n -u "$user" "$env" DBUS_SESSION_BUS_ADDRESS="$a" "$dbus_send" --session \
                --dest=org.freedesktop.DBus --type=method_call --print-reply --reply-timeout=20000 / \
                org.freedesktop.DBus.GetConnectionUnixProcessID "string:$sm_dest" | \
                sed -n -e 's/^ *uint32 \([0-9]*\) *$/\1/p')"
        if [ -n "$sm_pid" ] ; then
			logout="logout_kill_sm"
            return 0
        fi
    fi
    return 1
}

# more explicit tests
test_dbus_gnome() {
    typeset a="$1" ; shift
    if sudo -n -u "$user" "$env" DBUS_SESSION_BUS_ADDRESS="$a" "$dbus_send" --session --dest=org.gnome.SessionManager \
    --type=method_call --print-reply \
    --reply-timeout=20000  \
    '/org/gnome/SessionManager' \
    'org.freedesktop.DBus.Properties.Get' 'string:org.gnome.SessionManager' 'string:SessionName' ; then
        # it is gnome
        sm_dest='org.gnome.SessionManager'
        sm_path='/org/gnome/SessionManager'
        sm_method='org.gnome.SessionManager.Logout'
        sm_args='uint32:1'
        logout="logout_call_sm"
        return 0;
    fi
    return 1
}

test_dbus_mate() {
    typeset a="$1" ; shift
    if sudo -n -u "$user" "$env" DBUS_SESSION_BUS_ADDRESS="$a" "$dbus_send" --session --dest=org.mate.SessionManager \
    --type=method_call --print-reply \
    --reply-timeout=20000  \
    '/org/mate/SessionManager' \
    'org.mate.SessionManager.CanShutdown' ; then
        # it is mate
        sm_dest='org.mate.SessionManager'
        sm_path='/org/mate/SessionManager'
        sm_method='org.mate.SessionManager.Logout'
        sm_args='uint32:1'
        logout="logout_call_sm"
        return 0
    fi
    return 1
}

# Logout commands

logout_kill_sm() {
    sudo -n -u "$user" "$env" "$bin_kill" "$sm_pid"
}

logout_call_sm() {
    sudo -n -u "$user" "$env" DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" "$dbus_send" \
    --session --dest="$sm_dest" \
    --type=method_call --print-reply \
    --reply-timeout=20000  \
    "$sm_path" "$sm_method" $sm_args
}

logout_killall() {
    sudo -n -u "$user" "$env" "$killall" -u "$user"
}

logout_kill_X11() {
    for id in $(sudo -n -u "$user" "$env" XAUTHORITY="$XAUTHORITY" DISPLAY="$x11" "$xwininfo" -root -children -int | grep -v children | sed -n -e 's/^ *\([0-9]*\) .*$/\1/p') ; do
        sudo -n -u "$user" "$env" XAUTHORITY="$XAUTHORITY" DISPLAY="$x11" "$xkill" -id "$id"  2>/dev/null
    done
}

# locate the DBUS
DBUS_SESSION_BUS_ADDRESS=''
for pid in $(ps -u "$user" -o 'pid=') ; do
    environ="$(sudo -n -u "$user" "$cat" /proc/"$pid"/environ 2>/dev/null | tr '\0' '\n' )"
    if [ -n "$x11" ] ; then
        d="$(printf '%s\n' "$environ" | sed -n -e 's/DISPLAY=//p')"
        if [ "${d%.*}" != "${x11%.*}" ] ; then
            continue
        fi
    fi
    xa="$(printf '%s\n' "$environ" | sed -n -e 's/XAUTHORITY=//p')"
    if [ -n "$xa" ] ; then
        XAUTHORITY="$xa"
    fi
    a="$(printf '%s\n' "$environ" | sed -n -e 's/DBUS_SESSION_BUS_ADDRESS=//p')"
    if [ -n "$a" ] && { test_dbus_mate "$a" || test_dbus_gnome "$a" || test_dbus_universal "$a" ; } >/dev/null ; then
        DBUS_SESSION_BUS_ADDRESS="$a"
        break
    fi
done
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ] ; then
  if [ -n "$XAUTHORITY" ] ; then
      logout=logout_kill_X11
  else
      echo "Can't find the session dbus" 1>&2
      # terminate the watchdog. We do not need it any more
      kill -TERM "$wdpid" 2>/dev/null
      wait $wdpid 2>/dev/null
      exit 1
  fi
fi

# sudo -n -u "$user" "$env" DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" ; kill -TERM "$wdpid" 2>/dev/null ; wait $wdpid 2>/dev/null ; exit 99
if [ -n "$DBUS_SESSION_BUS_ADDRESS" ] ; then
    sudo -n -u "$user" "$env" DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" "$notify_send" -t 0 -u critical "Zeitüberschreitung" "Bitte jetzt abmelden" &
fi

typeset -i now="$(date '+%s')"
let 'end = now + left'
while ((now < end - warn2)); do
sudo -n "$env" "$play" -q /usr/share/sounds/freedesktop/stereo/service-login.oga \
    /usr/share/sounds/freedesktop/stereo/service-login.oga \
    gain -n 0.9 2>/dev/null
now="$(date '+%s')"
done
while ((now < end )); do
sudo -n "$env" "$play" -q /usr/share/sounds/freedesktop/stereo/complete.oga \
    gain -n 0.9 2>/dev/null
now="$(date '+%s')"
done

$logout

# terminate the watchdog. We do not need it any more
kill -TERM "$wdpid" 2>/dev/null
wait $wdpid 2>/dev/null

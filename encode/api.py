# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2009 Guillaume Pellerin <pellerin@parisson.com>
#
# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

from timeside.core import Interface, TimeSideError

class IEncoder(Interface):
    """Encoder driver interface"""

    # Remark: the method prototypes do not include any self or cls argument
    # because an interface is meant to show what methods a class must expose
    # from the caller's point of view. However, when implementing the class
    # you'll obviously want to include this extra argument.

    # FIXME: this constructor conflicts with the core component architecture
    def __init__(output, nchannels, samplerate):
        """The constructor must always accept the output, nchannels and samplerate 
        arguments.  It may accepts extra arguments such as bitrate, depth, etc.., 
        but these must be optionnal, that is have a default value.
        
        The output must either be a filepath or a callback function/method for 
        for the streaming mode. The callback must accept one argument which is 
        block of binary data.
        """

    def format():
        """Return the encode/encoding format as a short string
        Example: "MP3", "OGG", "AVI", ...
        """

    def description():
        """Return a string describing what this encode format provides, is good
        for, etc... The description is meant to help the end user decide what
        format is good for him/her
        """

    def file_extension():
        """Return the filename extension corresponding to this encode format"""

    def mime_type():
        """Return the mime type corresponding to this encode format"""

    def set_metadata(metadata):
        """metadata is a tuple containing tuples for each descriptor return by
        the dc.Ressource of the item, in the model order :
        ((name1, value1),(name2, value2),(name1, value3), ...)"""

    def update():
        """Updates the metadata into the file passed as the output argument
           to the constructor. This method can't be called in streaming
           mode."""

    def process(frames):
        """Encode the frames passed as a numpy array, where columns are channels.
        
           In streaming mode the callback passed to the constructor is called whenever
           a block of encoded data is ready."""

    def finish():
        """Flush the encoded data and close the output file/stream. Calling this method
        may cause the streaming callback to be called if in streaming mode."""
  
class EncodeProcessError(TimeSideError):

    def __init__(self, message, command, subprocess):
        self.message = message
        self.command = str(command)
        self.subprocess = subprocess

    def __str__(self):
        if self.subprocess.stderr != None:
            error = self.subprocess.stderr.read()
        else:
            error = ''
        return "%s ; command: %s; error: %s" % (self.message,
                                                self.command,
                                                error)

=============
 Quick start
=============

A most basic operation, transcoding, is easily performed with two processors:


.. testsetup:: test_1,test_2,test_3

   import timeside
   import os
   ModulePath =  os.path.dirname(os.path.realpath(timeside.analyzer.core.__file__))
   wavFile = os.path.join(ModulePath , '../../tests/samples/sweep.wav')
   decoder = timeside.decoder.file.FileDecoder(wavFile)

.. testcleanup:: test_1

   os.remove('sweep.ogg')

.. testcleanup:: test_2

   os.remove('graph.png')

.. testcleanup:: test_3

   os.remove('sweep.mp3')
   os.remove('sweep.flac')

.. doctest:: test_1

 >>> import timeside
 >>> from timeside.core import get_processor	     
 >>> decoder = get_processor('gst_dec')('sweep.wav')# doctest: +SKIP
 >>> encoder = get_processor('gst_vorbis_enc')('sweep.ogg')
 >>> pipe = decoder | encoder
 >>> pipe.run()

As one can see in the above example, creating a processing pipe is performed with
the binary OR operator.

Audio data visualisation can be performed using graphers, such as Waveform and
Spectrogram. All graphers return an image:

.. doctest:: test_2

   >>> import timeside
   >>> from timeside.core import get_processor
   >>> decoder =  get_processor('gst-dec')('sweep.wav') # doctest: +SKIP
   >>> spectrogram = get_processor('spectrogram_lin')(width=400, height=150)
   >>> (decoder | spectrogram).run()
   >>> spectrogram.render('graph.png')

It is possible to create longer pipes, as well as subpipes, here for both
analysis and encoding:

.. doctest:: test_3

   >>> import timeside
   >>> from timeside.core import get_processor
   >>> decoder = get_processor('gst-dec')('sweep.wav') # doctest: +SKIP
   >>> levels = get_processor('level')()
   >>> encoders = get_processor('gst_mp3_enc')('sweep.mp3') | get_processor('gst_flac_enc')('sweep.flac')
   >>> (decoder | levels | encoders).run()
   >>> print levels.results
   {'level.max': GlobalValueResult(id_metadata=IdMetadata(id='level.max', name='Level Max', unit='dBFS', description='', date='...', version='...', author='TimeSide', uuid='...'), data_object=DataObject(value=array([-6.021])), audio_metadata=AudioMetadata(uri='file://...sweep.wav', start=0.0, duration=8.0, is_segment=False, sha1='...', channels=2, channelsManagement=''), parameters={}), 'level.rms': GlobalValueResult(id_metadata=IdMetadata(id='level.rms', name='Level RMS', unit='dBFS', description='', date='...', version='...', author='TimeSide', uuid='...'), data_object=DataObject(value=array([-9.856])), audio_metadata=AudioMetadata(uri='file://...sweep.wav', start=0.0, duration=8.0, is_segment=False, sha1='...', channels=2, channelsManagement=''), parameters={})}

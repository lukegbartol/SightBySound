
It works by using sox to recode whatever format you give it to 22050Hz, mono, 16 bits. Then, for azimuth steps of 5 degrees it applies the HRTF filters to produce the left and right channels, and writes a wav file out. Then it uses sox again to encode the wav file to ogg and mp3 formats.

You'll need python + numpy + scipy + sox to use this.

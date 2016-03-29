#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile;

class FileWriterSR:
  def __init__(self, filename):
    self.file = zipfile.ZipFile(filename, "w")
    
  def set_sample_rate(self, sample_rate):
    if(sample_rate > 10**9):
      self.sample_rate = "%i GHz" % (sample_rate / 10**9);
    elif(sample_rate > 10**6):
      self.sample_rate = "%i MHz" % (sample_rate / 10**6);
    elif(sample_rate > 10**3):
      self.sample_rate = "%i KHz" % (sample_rate / 10**3);
    else:
      self.sample_rate = "%i Hz"  % (sample_rate);
    
  def write_header(self):
    self.file.writestr('version', '2');
    self.file.writestr('metadata',
                       "[global]\n"
                       "sigrok version=0.4.0\n"
                       "\n"
                       "[device 1]\n"
                       "capturefile=logic-1\n"
                       "unitsize=1\n"
                       "total probes=8\n"
                       "samplerate=%s\n"
                       "probe1=0\n"
                       "probe2=1\n"
                       "probe3=2\n"
                       "probe4=3\n"
                       "probe5=4\n"
                       "probe6=5\n"
                       "probe7=6\n"
                       "probe8=7\n"
                       "\n" % self.sample_rate); 
    
  def write_samples(self, samples=[]):
    # Extract MSB
    stream = bytearray(len(samples));
    index = 0;      
    for sample in samples:
      stream[index] = sample & 0xff;
      index = index + 1;
    self.file.writestr('logic-1-1', buffer(stream));

  def close(self):
    self.file.close()
    self.file = None;

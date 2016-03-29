#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FileWriterOLS:
  def __init__(self, filename):
    self.file = open(filename, "w");
    
  def set_sample_rate(self, sample_rate):
    self.sample_rate = sample_rate;
    
  def write_header(self):
    self.file.write(";Rate: %i\n" % int(self.sample_rate));
    self.file.write(";Channels: 16\n");
    self.file.write(";EnabledChannels: -1\n");
    self.file.write(";CursorEnabled: false\n");
    
  def write_samples(self, samples=[]):    
    index = 0;
    for sample in samples:
      self.file.write("%s@%i\n" % (format(sample, '08x'), index));
      index = index + 1;

  def close(self):
    self.file.close();
    self.file = None;

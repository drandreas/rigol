#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys as sys;
import visa as visa;

DEBUG = 0

class Rigol:
  def __init__(self, ip):
    self.rm = visa.ResourceManager();
    self.scope = self.rm.open_resource("TCPIP::%s::INSTR" % ip);
    
  def debug(self, msg):
    if DEBUG:
      print >>sys.stderr, "%s" % msg;
      
  def stop(self):
    self.scope.write(":STOP")

  def query_idn(self):
    return self.scope.query("*IDN?").strip();    

  def query_enabled_channels(self):
    enabled_channels = 0
    for index in range(0, 16):
      channel = int(self.scope.query(":LA:DISP? D%i" % index));
      enabled_channels |= (channel << index)
    return enabled_channels

  def query_channel_labels(self):
    labels = [];
    for index in range(0, 16):
      label = self.scope.query(":LA:DIG%i:LAB?" % index);
      if("No Label!" in label):
        labels.append("D%i" % index);
      else:
        labels.append(str(label.strip()));
    return labels;
  
  def query_memory_depth(self):
    return int(self.scope.query(":ACQ:MDEP?"));

  def query_sample_rate(self):
    return float(self.scope.query(":ACQ:SRAT?"));
  
  def query_frame_count(self):
    return int(self.scope.query(":FUNCtion:WREPlay:FMAX?"));
  
  def select_frame(self, frame):
    self.scope.write(":FUNCtion:WREPlay:FCURrent %i" % frame);
    return int(self.scope.query("FUNCtion:WREPlay:FCURrent?"));
 
  def query_samples(self, channel="LA", mode="NORM", points=1400, datatype="H"):
    # Stop oscilloscope
    self.stop();
    
    # Prepare oscilloscope for reading 
    self.scope.write(":WAV:SOUR %s" % channel);
    self.scope.write(":WAV:MODE %s" % mode);
    self.scope.write(":WAV:POIN %i" % points);
    self.scope.write(":WAV:FORM BYTE");
    self.debug(":WAV:POIN? => %i" % int(self.scope.query(":WAV:POIN?")))

    samples = [];
    try:
      # Read
      self.scope.write(":WAV:RES")
      self.scope.write(":WAV:BEG")
    
      while True:
        status = self.scope.query(":WAV:STAT?").strip();
        self.debug(":WAV:STAT? => %s" % status)
        if("IDLE" in status):
          samples.extend(self.scope.query_binary_values(":WAV:DATA?", datatype=datatype, is_big_endian=False));
          print >>sys.stderr, "Progress: %i of %i samples" % (len(samples), points);
          break;
        elif("READ" in status):
          samples.extend(self.scope.query_binary_values(":WAV:DATA?", datatype=datatype, is_big_endian=False));
          print >>sys.stderr, "Progress: %i of %i samples" % (len(samples), points);
    finally:
      # Cleanup    
      self.scope.write(":WAV:END")
    return samples;
  
  def close(self):
    self.scope.close()

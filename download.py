#!/usr/local/bin/python2.7
# encoding: utf-8

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from Rigol import Rigol
from FileWriterOLS import FileWriterOLS
from FileWriterSR import FileWriterSR

def main():
  scope       = None;
  file_writer = None;
  try:
    # Setup argument parser
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter);
    parser.add_argument(dest="ip",                          help="IP address of oscilloscope",            metavar="ip");
    parser.add_argument(dest="filename",                    help="File to write samples to",              metavar="filename");
    parser.add_argument(dest="format",                      help="File format to use (Options: sr, ols",  metavar="format");
    parser.add_argument("--all-frames",  dest="all",        help="Download all available frames",         default=False, action='store_true');
    parser.add_argument("--scale",       dest="scale",      help="scale sample rate by s (default: 1.0)", metavar="s", default=1.0);
    parser.add_argument("--sample-rate", dest="samplerate", help="overwrite samplerate",                  metavar="r");

    # Process arguments
    args = parser.parse_args();
    
    # Connect to oscilloscope 
    scope = Rigol(args.ip);
    sample_rate = scope.query_sample_rate();
    
    samples = []
    if(args.all):
      frames = scope.query_frame_count();
      for frame in range(1, frames+1):
        scope.select_frame(frame);
        print >>sys.stderr, "Progress: %i of %i frames" % (frame, frames);
        samples.extend(scope.query_samples("LA", "RAW", sample_rate));
    else:
      samples.extend(scope.query_samples("LA", "RAW", sample_rate));
    
    # Write file
    if(args.format == "sr"):
      file_writer = FileWriterSR(args.filename);
    else:
      file_writer = FileWriterOLS(args.filename);
    
    if(args.samplerate is not None):
      file_writer.set_sample_rate(int(args.samplerate));
    else:
      file_writer.set_sample_rate(sample_rate*float(args.scale));
    file_writer.write_header();
    file_writer.write_samples(samples);
    file_writer.close();

    # Cleanup
    scope.close();
    
  except KeyboardInterrupt:
    # Handle keyboard interrupt
    return 1;
  
if __name__ == "__main__":
  sys.exit(main());

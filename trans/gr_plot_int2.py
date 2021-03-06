#!/usr/bin/envpython

#

#Copyright 2007,2008,2011 Free Software Foundation, Inc.

#

#This file is part of GNU Radio

#

#GNU Radio is free software; you can redistribute it and/or modify

#it under the terms of the GNU General Public License as published by

#the Free Software Foundation; either version 3, or (at your option)

#any later version.

#

#GNU Radio is distributed in the hope that it will be useful,

#but WITHOUT ANY WARRANTY; without even the implied warranty of

#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

#GNU General Public License for more details.

#

#You should have received a copy of the GNU General Public License

#along with GNU Radio; see the file COPYING. If not, write to

#the Free Software Foundation, Inc., 51 Franklin Street,

#Boston, MA 02110-1301, USA.

#

"""

Utilityto help plotting data from files.

"""

 

try:

    import scipy

except ImportError:

    print "Please install SciPy to runthis script (http://www.scipy.org/)"

    raise SystemExit, 1

 

try:

    from pylab import *

except ImportError:

    print "Please install Matplotlib torun this script (http://matplotlib.sourceforge.net/)"

    raise SystemExit, 1

 

from optparse import OptionParser

 

class plot_data:

    def __init__(self, datatype, filenames,options):

        self.hfile = list()

        self.legend_text = list()

        for f in filenames:

            self.hfile.append(open(f,"r"))

            self.legend_text.append(f)

 

        self.block_length = options.block

        self.start = options.start

        self.sample_rate = options.sample_rate

 

        self.datatype = datatype

        self.sizeof_data =datatype().nbytes    # number of bytesper sample in file

 

        self.axis_font_size = 16

        self.label_font_size = 18

        self.title_font_size = 20

        self.text_size = 22

 

        # Setup PLOT

        self.fig = figure(1, figsize=(16, 9),facecolor='w')

        rcParams['xtick.labelsize'] =self.axis_font_size

        rcParams['ytick.labelsize'] =self.axis_font_size

 

        self.text_file_pos = figtext(0.10,0.88, "File Position: ", weight="heavy",size=self.text_size)

        self.text_block    = figtext(0.40, 0.88, ("Block Size:%d" % self.block_length),

                                    weight="heavy", size=self.text_size)

        self.text_sr       = figtext(0.60, 0.88, ("SampleRate: %.2f" % self.sample_rate),

                                    weight="heavy", size=self.text_size)

        self.make_plots()

 

        self.button_left_axes =self.fig.add_axes([0.45, 0.01, 0.05, 0.05], frameon=True)

        self.button_left =Button(self.button_left_axes, "<")

        self.button_left_callback =self.button_left.on_clicked(self.button_left_click)

 

        self.button_right_axes =self.fig.add_axes([0.50, 0.01, 0.05, 0.05], frameon=True)

        self.button_right =Button(self.button_right_axes, ">")

        self.button_right_callback =self.button_right.on_clicked(self.button_right_click)

 

        self.xlim = self.sp_f.get_xlim()

        print 'start!'

        self.manager = get_current_fig_manager()

        connect('key_press_event', self.click)

        show()

 

    def get_data(self, hfile):

        self.text_file_pos.set_text("FilePosition: %d" % (hfile.tell()//self.sizeof_data))

        try:

            f = scipy.fromfile(hfile,dtype=self.datatype, count=self.block_length)

        except MemoryError:

            print "End of File"

        else:

            self.f = scipy.array(f)

            self.time =scipy.array([i*(1/self.sample_rate) for i in range(len(self.f))])

            fhh2 = open(r'./kk.txt', 'w')

            print str(len(self.f))

            data = []

            for j in range(len(self.f)):

            	data.append((self.f[j]))

            	fhh2.write(str(data))
	    
            fhh2.close()

 

    def make_plots(self):

        self.sp_f = self.fig.add_subplot(2,1,1,position=[0.075, 0.2, 0.875, 0.6])

        self.sp_f.set_title(("Amplitude"),fontsize=self.title_font_size, fontweight="bold")

        self.sp_f.set_xlabel("Time(s)", fontsize=self.label_font_size, fontweight="bold")

        self.sp_f.set_ylabel("Amplitude(V)", fontsize=self.label_font_size, fontweight="bold")

        self.plot_f = list()

 

        maxval = -1e12

        minval = 1e12

 

        for hf in self.hfile:

            # if specified on the command-line,set file pointer

           	hf.seek(self.sizeof_data*self.start, 1)

 
          	self.get_data(hf)

 

            # Subplot for real and imaginaryparts of signal

          	self.plot_f += plot(self.time, self.f,'o-')
            	maxval = max(maxval, self.f.max())

            	minval = min(minval, self.f.min())

 

        self.sp_f.set_ylim([1.5*minval,1.5*maxval])

 

        self.leg =self.sp_f.legend(self.plot_f, self.legend_text)

 

        draw()

 

    def update_plots(self):

        maxval = -1e12

        minval = 1e12

        for hf,p in zip(self.hfile,self.plot_f):

            self.get_data(hf)

            p.set_data([self.time, self.f])

            maxval = max(maxval, self.f.max())

            minval = min(minval, self.f.min())

 

        self.sp_f.set_ylim([1.5*minval,1.5*maxval])

 

        draw()

 

    def click(self, event):

        forward_valid_keys = [" ","down", "right"]

        backward_valid_keys = ["up","left"]

 

        if(find(event.key,forward_valid_keys)):

            self.step_forward()

 

        elif(find(event.key,backward_valid_keys)):

            self.step_backward()

 

    def button_left_click(self, event):

        self.step_backward()

 

    def button_right_click(self, event):

        self.step_forward()

 

    def step_forward(self):

        self.update_plots()

 

    def step_backward(self):

        for hf in self.hfile:

            # Step back in file position

            if(hf.tell() >=2*self.sizeof_data*self.block_length ):

               hf.seek(-2*self.sizeof_data*self.block_length, 1)

            else:

                hf.seek(-hf.tell(),1)

        self.update_plots()

 

 

def find(item_in, list_search):

    try:

       return list_search.index(item_in) != None

    except ValueError:

       return False

 

try:

    import scipy

except ImportError:

    print "Please install SciPy to runthis script (http://www.scipy.org/)"

    raise SystemExit, 1

 

from optparse import OptionParser

def main():

    usage="%prog: [options] input_filenames"

    description = "Takes a GNU Radiointeger binary file and displays the samples versus time. You can set the blocksize to specify how many points to read in at a time and the start position inthe file. By default, the system assumes a sample rate of 1, so in time, eachsample is plotted versus the sample number. To set a true time axis, set thesample rate (-R or --sample-rate) to the sample rate used when capturing thesamples."

 

    parser =OptionParser(conflict_handler="resolve", usage=usage,description=description)

    parser.add_option("-B","--block", type="int", default=1000,

                      help="Specify theblock size [default=%default]")

    parser.add_option("-s","--start", type="int", default=0,

                      help="Specify where to start in the file[default=%default]")

    parser.add_option("-R","--sample-rate", type="float", default=1.0,

                      help="Set thesampler rate of the data [default=%default]")

 

    (options, args) = parser.parse_args ()

    if len(args) < 1:

        parser.print_help()

        raise SystemExit, 1

    filenames = args

 

    datatype=scipy.int32

    dc = plot_data(datatype, filenames,options)

 

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        pass

# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
#  Copyright © 2015-2016 VMware, Inc. All Rights Reserved.                    #
#                                                                             #
#  Licensed under the BSD 2-Clause License (the “License”); you may not use   #
#  this file except in compliance with the License.                           #
#                                                                             #
#  The BSD 2-Clause License                                                   #
#                                                                             #
#  Redistribution and use in source and binary forms, with or without         #
#  modification, are permitted provided that the following conditions are met:#
#                                                                             #
#  - Redistributions of source code must retain the above copyright notice,   #
#      this list of conditions and the following disclaimer.                  #
#                                                                             #
#  - Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the    #
#      documentation and/or other materials provided with the distribution.   #
#                                                                             #
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"#
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  #
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE #
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  #
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR        #
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF       #
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS   #
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN    #
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)    #
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF     #
#  THE POSSIBILITY OF SUCH DAMAGE.                                            #
# ----------------------------------------------------------------------------#

from liota.boards import gateway
from liota.boards.gateway_dk300 import Dk300
from liota.dcc.graphite_dcc import Graphite
from liota.transports.socket_connection import Socket

from temper import TemperHandler

# getting values from conf file
config = {}
execfile('sampleProp.conf', config)


#---------------------------------------------------------------------------


def getTemp():
    th = TemperHandler()
    devs = th.get_devices()
    t = devs[0].get_temperatures()
    return  t[0]['temperature_c']

#--------------------------------------------------------------------------
# In this example, we demonstrate how data from a simulated device generating 
# random numbers can be directed to graphite data center component using Liota.
# The program illustrates the ease of use Liota brings to IoT application developers.

if __name__ == '__main__':

    gateway = Dk300(config['Gateway1Name'])

    # Sending data to an alternate data center component (e.g. data lake for analytics)
    # Graphite is a data center component
    # Socket is the transport which the agent uses to connect to the graphite instance
    graphite = Graphite(Socket(config['GraphiteIP'], config['GraphitePort']))
    tempMetric = graphite.create_metric(gateway, 'Temperature C', unit=None, sampling_interval_sec=10, aggregation_size=1, sampling_function=getTemp)
    tempMetric.start_collecting()


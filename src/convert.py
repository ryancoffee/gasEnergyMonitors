#!/sdf/sw/images/slac-ml/20211027.1/bin/python3
import h5py
import numpy as np
import scipy.io 
import scipy.fft
import argparse
import re
import argparse

parser = argparse.ArgumentParser(description='Converter GDET from .mat files to .h5\nmain -infiles <files separated by sapce | globbed filenames>')
parser.add_argument('-infiles',   type=str, nargs='+',required=True, help='input files')


def main():
    args,unknown = parser.parse_known_args()
    if len(unknown)>0:
        _ = [print('unknown arg: %s'%u) for u in unknown]
        return
    for fname in args.infiles:
        m = re.search('(^.+)/(.+).mat',fname)
        if m:
            path = m.group(1)
            fnamehead = m.group(2)
            h5name = '%s/%s.h5'%(path,fnamehead)
            with h5py.File(h5name,'w') as f:
                mat = scipy.io.loadmat(fname)
                #print(mat.keys())
                #_ = [print(i,mat['data'][0][0][i]) for i in range(len(mat['data'][0][0]))]
                #0 = data
                #1 = shotnum
                #2 = time since start (span usually 1 second with 120 shots)
                #3 = n something
                #4 = nk?
                #5 = Photon Energy
                #6 = timestamp
                gdets = f.create_dataset('gdets',data = mat['data'][0][0][0].astype(np.uint16),dtype=np.uint16)
                gdets.attrs.create('shotIDs',data = mat['data'][0][0][1])
                gdets.attrs.create('shotTimes',data = mat['data'][0][0][2])
                gdets.attrs.create('PhotonEn_eV',data= mat['data'][0][0][5])
                gdets.attrs.create('timeStamp',data = str(mat['data'][0][0][6]))
                if (mat['data'][0][0][5] > 2500): # this is per Franz-Josef Decker
                    gdets.attrs.create('sampling_MSps',data = np.uint16(1000))
                else:
                    gdets.attrs.create('sampling_MSps',data = np.uint16(395))
                freqs = f.create_dataset('freqs',data = np.abs(scipy.fft.fft((mat['data'][0][0][0] - np.mean(mat['data'][0][0][0][:,:100,:100])).astype(np.int32) , axis = 1) ).real.astype(np.uint16),dtype=np.uint16)
                #labels = f.create_group('labels')
                #_ = [ print(str(lbl)) for lbl in mat['data'][-1] ]
                    #gdets.attrs.create('labels',data = [str(lbl) for lbl in mat['data'][0][0][-1][0]])
    return

if __name__ == '__main__':
    main()


'''
mat['data'][0][0][0].shape
>> mat['data'][0][0][0].shape
(4, 800, 120)
>>> mat['data'][0][0][1].shape
(1, 120)
>>> mat['data'][0][0][2].shape
(1, 120)
>>> mat['data'][0][0][2]
array([[7.250000e-04, 5.279000e-03, 1.396600e-02, 2.162900e-02,
        3.002300e-02, 3.832800e-02, 4.661200e-02, 5.505500e-02,
        7.187600e-02, 7.908800e-02, 8.749000e-02, 9.736200e-02,
        1.046940e-01, 1.143850e-01, 1.227850e-01, 1.321150e-01,

4 channels of GDET, 800 shots I guess, 120 time bins maybe?

dtype=[('gg', 'O'), ('t', 'O'), ('dt', 'O'), ('n', 'O'), ('nk', 'O'), ('Eph', 'O'), ('t_stamp', 'O')])
I think this tells me the list of data:
gasdets
time
dtime
n
nk ?
ePhoton
timestamp
 
'''

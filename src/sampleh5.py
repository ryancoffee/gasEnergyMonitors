#!/sdf/sw/images/slac-ml/20211027.1/bin/python3
import h5py
import numpy


_= [ np.savetxt( './figs/samples_gdet%i_ph%i.dat'%(c,f['gdets'].attrs['PhotonEn_eV']), f['gdets'][()][c,:,:] , fmt='%i' ) for c in range(f['gdets'][()].shape[0]) ]

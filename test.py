from numpy import *
import scipy as sp
from scipy import interpolate
import tdpy.mcmc

def retr_llik_flag(sampvarb):
        
    xpos = sampvarb[0]
    ypos = sampvarb[1]

    llik = sp.interpolate.interp2d(xgrd, ygrd, pdfn)(xpos, ypos)
    sampcalc = [arange(5), arange(6)]

    return llik, sampcalc


def retr_datapara():
    
    numbpara = 2
    
    datapara.indx['xpos'] = 0
    datapara.indx['ypos'] = 0
    datapara.name[0] = 'xpos'
    datapara.name[1] = 'ypos'
    datapara.minm[:] = 0.
    datapara.maxm[:] = 1.
    datapara.scal[:] = 'self'
    datapara.labl[0] = r'$x$'
    datapara.labl[1] = r'$y$'
    datapara.unit[:] = ''
    datapara.vari[:] = 1e-1
    datapara.true[:] = None
    datapara.strg = datapara.labl + ' ' + datapara.unit

                                
# target PDF
path = path = os.environ["TDPY_DATA_PATH"] + '/turkflag.png'
imag = sp.ndimage.imread(path)
rati = float(imag.shape[0]) / imag.shape[1]
xinp = linspace(0., 1., imag.shape[1])
yinp = linspace(0., 1., imag.shape[0])
numbxgrd = 200
numbygrd = int(200 * rati)
xgrd = linspace(0., 1., numbxgrd)
ygrd = linspace(0., 1., numbygrd)
imag = sp.ndimage.gaussian_filter(imag, sigma=[xinp.size / 100, yinp.size / 100, 0])
pdfn = zeros((numbygrd, numbxgrd, 3))
for k in range(3):
    pdfn[:, :, k] = sp.interpolate.interp2d(xinp, yinp, imag[:, :, k])(xgrd, ygrd)
pdfn = 0.3 * pdfn[:, :, 0]

figr, axis = plt.subplots()
axis.imshow(imag, extent=[0., 1., 0., 1.], interpolation='none', aspect=rati)
plt.savefig('imag.pdf')
plt.close(figr) 

figr, axis = plt.subplots()
imag = axis.imshow(pdfn, extent=[0., 1., 0., 1.], interpolation='none', aspect=rati)
plt.colorbar(imag)
plt.savefig('targ.pdf')
plt.close(figr) 

# MCMC setup
verbtype = 1
numbproc = 2
numbswep = 7
datapara = retr_datapara()
optiprop = True
pathbase = '/Users/tansu/Desktop/'

# run MCMC
sampbund = tdpy.mcmc.init(numbproc, numbswep, retr_llik_flag, datapara, pathbase=pathbase, optiprop=True, verbtype=verbtype, rtag='flag')
listxpos = sampbund[0][:, 0]
listypos = sampbund[0][:, 1]
numbsamp = listxpos.size
pathtemp = pathbase + 'post'
numbfram = 10
for k in range(numbfram):
    indxsamp = int(numbsamp * float(k) / numbfram)
    figr, axis = plt.subplots()
    axis.scatter(listxpos[:indxsamp], listypos[:indxsamp], s=3)
    axis.set_xlim([0., 1.])
    axis.set_ylim([0., 1.])
    path = pathtemp + '%04d.pdf' % k
    plt.savefig(path)
    plt.close(figr) 

cmnd = 'convert -delay 20 %s*.pdf post.gif' % pathtemp
os.system(cmnd)




# define the likelihood function
def retr_llik(sampvarb):
        
    xpos = sampvarb[0]
    ypos = sampvarb[1]

    llik = sp.interpolate.interp2d(xgrd, ygrd, pdfn)(xpos, ypos)

    return llik

    
# define the target PDF
xgrd = linspace(0., 2. * pi, 100)
ygrd = linspace(0., 2. * pi, 100)
pdfn = exp(sin(xgrd[:, None]) * sin(ygrd[None, :]))

# construct the parameter object
datapara = tdpy.util.datapara(2)
datapara.defn_para('xpos', 0., 1., 'self', r'$x$', '', None, None)
datapara.defn_para('ypos', 0., 1., 'self', r'$y$', '', None, None)

# run MCMC
sampbund = tdpy.mcmc.init(retr_llik, datapara)

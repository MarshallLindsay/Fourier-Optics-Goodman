#Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import scipy as sc
import pint

plt.style.use(['science'])
u = pint.UnitRegistry()


#Define the radiating point source
def point_source(x=0,y=0,wavelength=500*u.nm, amplitude = 1):
    wavenumber = (2*np.pi / wavelength)
    return amplitude * np.exp(1j * wavenumber * np.sqrt(x**2 + y**2))



#Test our point source with a meshgrid

#Wavelength of interest
wavelength = 500 * u.nm

yoffset = 0*u.um
xoffset = 0*u.um

resolution = 1000 #Might need to adjust this
x = np.linspace(-2.5, 2.5, resolution) * u.um
xx,yy = np.meshgrid(x,x)

#Run the point source with the meshgrid
z = point_source((xx-xoffset),(yy-yoffset),wavelength)

plt.figure(figsize=(5,5))
plt.pcolormesh(xx,yy,np.real(z.magnitude),cmap='inferno')
plt.title("Spherical Point Source")
plt.xlabel("X-Position [um]")
plt.ylabel("Y-Position [um]")
plt.show()


#Define the figure
fig,ax = plt.subplots(1,3,figsize=(12,6), dpi=90)

ax[0].set_title("Spherical Radiating Point Source\n"\
            r"$U = \exp{\left[j\frac{2\pi}{\lambda}\sqrt{(x-x_0)^2 + (y-y_0)^2}\right]}$", fontsize=12)
ax[0].set_xlabel("Position [um]") #The units are hard coded - need a function to determine them
ax[0].set_ylabel("Position [um]")

#Set intial plot
im0 = ax[0].pcolormesh(xx,yy,np.real(z.magnitude), cmap='inferno')
vl_loc = 0
vl0 = ax[0].vlines(vl_loc, ymin=-2.5, ymax = 2.5, linewidth=2, color='blue')

#Make room for sliders
fig.subplots_adjust(left= 0.1,bottom = 0.3)

#Define some sliders
wavelength_slider_ax = fig.add_axes([0.09, 0.2, 0.2, 0.03])
wavelength_slider = Slider(wavelength_slider_ax, r'$\lambda$', 
                            (200*u.nm).magnitude, 
                            (1550*u.nm).magnitude, 
                            valinit=wavelength.magnitude)
wavelength_slider.label.set_size(12)

yoffset_slider_ax = fig.add_axes([0.09, 0.175, 0.2, 0.03])
yoffset_slider = Slider(yoffset_slider_ax, r"$y_0$", 
                        (-2.5*u.um).magnitude, 
                        (2.5*u.um).magnitude, 
                        valinit=yoffset.magnitude)
yoffset_slider.label.set_size(12)

xoffset_slider_ax = fig.add_axes([0.09, 0.15, 0.2, 0.03])
xoffset_slider = Slider(xoffset_slider_ax, r"$x_0$", 
                        (-2.5*u.um).magnitude, 
                        (2.5*u.um).magnitude, 
                        valinit=yoffset.magnitude)
xoffset_slider.label.set_size(12)

vloc_slider_ax = fig.add_axes([0.09, 0.075, 0.2, 0.03])
vloc_slider = Slider(vloc_slider_ax, "vl_loc", 
                        -2.5, 
                        2.5, 
                        valinit=vl_loc)
vloc_slider.label.set_size(12)


ax[1].set_title("Projection of Point Source onto the Line")
projection = np.real(z.magnitude)[:,500+int(vl_loc*100)]
im1 = ax[1].plot(x, projection)


ax[2].set_title("Frequency spectrum of QPF")
kx = np.fft.fftfreq(len(projection), np.diff(projection)[0])
kx = np.fft.fftshift(kx)
freq = np.fft.fft(projection)
freq = np.fft.fftshift(freq)
freq = np.abs(freq) ** 2
line = ax[2].plot(kx, freq)


def sliders_on_changed(val):
    z = point_source((xx-(xoffset_slider.val*u.um)), 
                     (yy-(yoffset_slider.val*u.um)), 
                     wavelength_slider.val*u.nm)
    #Point Source
    im0.set(array=np.real(z.magnitude))
    
    #Verticle Line
    vl0.set_segments([np.asarray([[vloc_slider.val, -2.5],[vloc_slider.val, 2.5]])])

    #Projection on the Line
    projection = np.real(z.magnitude)[:,500+int(vloc_slider.val*100)]
    im1[0].set_data(x, projection)

    #Frequency Spectrum
    freq = np.fft.fft(projection)
    freq = np.fft.fftshift(freq)
    freq = np.abs(freq) ** 2 
    line[0].set_data(kx,freq)
    ax[2].set_ylim(0,np.max(freq))
    
    fig.canvas.draw_idle()
    
wavelength_slider.on_changed(sliders_on_changed)
yoffset_slider.on_changed(sliders_on_changed)
xoffset_slider.on_changed(sliders_on_changed)
vloc_slider.on_changed(sliders_on_changed)

plt.show()

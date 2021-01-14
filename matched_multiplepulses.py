from scipy.fftpack import fft, ifft, fftshift
#from scipy import conj, linspace, exp
from scipy.constants import pi
from matplotlib import pyplot as plt
from numpy import linspace,exp,conj

def generate_signals(R,fc,BWf,t1,t2, num_samples):
    t = linspace(t1, t2,num_samples) # Pulsewidth (s)
    Td=t2-t1
    c=3e8
    t0=2*R/c
    Kchirp = BWf/Td;              #chirp pulse parameter 
    st = exp(1j*2*pi*(fc*t+Kchirp/2*(t**2))) # transmited signal 
    sr=exp(1j*2*pi*(fc*(t-t0)+Kchirp/2*(t-t0)**2)) # recieved signal 
    mean = 0
    std = 1 
    GWN = numpy.random.normal(mean, std, size=num_samples)
    sr=sr+GWN
    return(st,sr,t)
def matched_filter(st,sr):
    Hf = fft(conj(st))
    Si = fft(sr)
    so = fftshift(ifft(Si * Hf)) 
    return(so)


st,sr,t=generate_signals(R=4e2 ,fc=8e8,BWf=10e6,t1=-2.5e-6,t2=2.5e-6, num_samples=400)
st2,sr2,t2=generate_signals(R=8e2 ,fc=8e8,BWf=10e6,t1=-2.5e-6,t2=2.5e-6, num_samples=400)
so=matched_filter(st,sr)
so2=matched_filter(st2,sr2)
buffer=numpy.zeros(400)
pulses=numpy.append(buffer,so)
pulses=numpy.append(pulses,buffer)
pulses=numpy.append(pulses,so2)
pulses=numpy.append(pulses,buffer)

plt.figure(1)
plt.plot(t,st.real)
plt.title('transmitted signal for range=4e2')
plt.xlabel('Time Delay (s)')
plt.ylabel('real part')
plt.show()
plt.figure(1)
plt.plot(t, sr.real)
plt.title('recieved signal for range=4e2')
plt.xlabel('Time Delay (s)')
plt.ylabel('real part')
plt.show()
plt.plot(t2, st2.real)
plt.title('transmitted signal for range=8e2')
plt.xlabel('Time Delay (s)')
plt.ylabel('real part')
plt.show()
plt.figure(1)
plt.plot(t2, sr2.real)
plt.title('recieved signal for range=8e2')
plt.xlabel('Time Delay (s)')
plt.ylabel('real part')
plt.show()
plt.figure(1)
totaltime=numpy.array(range(len(pulses)))*1.25e-8
plt.plot(totaltime,abs(pulses))
plt.title('matched filter output(allpulses)')
#plt.xlabel('Time Delay (s)')
plt.xlabel('Time(sec)')
plt.ylabel('Amplitude')
plt.show()






from yt.mods import *
import matplotlib.pyplot as plt

def CenOstrikerKernel(x):
    ''' Here x is the current time minus the formation time normalized by the dynamical time'''
    # Enforce 0<=x<=10. x must be positive to avoid counting star formation from the future.
    # Meanwhile, x larger than 10 would yield very small values anyway, so we just set K(x)=0 in that case.
    np.clip(x, 0.0, 10.0, out=x)
    return np.exp(-x)*x

def sfrFromParticles(pf,data,theParticles,minDynamicalTime=0,times=None,kernel=CenOstrikerKernel, secondaryFilter=None):
    ''' Given a parameter file, a data source, and an array which indexes which particles to include in this analysis,
        compute the star formation rate as a function of time.
        
        Returns: an array of times (in years) and SFRs (in solar masses per year)
        
        Assumes that all particles have (initially) the same mass. I.e. I don't attempt to back out the initial mass
        by inverting the Cen & Ostriker formula, since I'm typically not using that prescription for feedback.
        
        Optional arguments:
        minDynamicalTime -- when we smooth out the star particle creation events over the Kernel (see below), 
                            we need a dynamical time. This is taken to be the maximum of the particle's recorded
                            dynamical time and this parameter for each particle.
        times            -- times is the array of times at which we will compute the SFR. By default, we take each
                            particle and sample the SFR at the time the particle is created, then at several increments of
                            that particle's dynamical time. This ensures that even at very low star formation rates, you will
                            see something resembling a continuous distribution, I think. This parameter lets you sidestep that
                            whole process and provide your own array. Especially useful if you only want the instantaneous SFR
                            at one time.
        kernel           -- Stars are formed one particle at a time in the simulation, so to get a continuous function SFR(t)
                            we need to smooth the star formation event of gas from the grid being converted into a particle
                            over some kernel. The kernel
                            1) should integrate to 1
                            2) is given a numpy array of x's, where x=(t-tCreation)/tDynamical
                            3) is by default the Cen & Ostriker (1992) kernel x*e^-x when x>=0, and 0 otherwise
        secondaryFilter  -- If two filters are applied to the original data source 'data', include the second one here.
                            This allows constructions like dd[particlesInCylinder][starParticles], where starParticles 
                            is the same length as the number of ones in particlesInCylinder, and picks out only the star particles
                            in the cylinder. By default this is set to None, which means the secondary filter will not do any
                            additional filtering.
    '''
    # If we haven't been given a secondaryFilter, construct a mask which lets through every particle.
    if secondaryFilter is None:
        secondaryFilter = np.ones(np.sum(theParticles),dtype=bool) # A secondary filter which will include all particles.

    # Collect relevant pieces of data for each particle
    creationTime = data['creation_time'][theParticles][secondaryFilter]*pf['years'] # units of years
    dynamicalTime = data['dynamical_time'][theParticles][secondaryFilter]*pf['years'] # units of years
    currentTime = pf['InitialTime']*pf['years']  
    
    # The following line simply enforces dynamicalTime >= minDynamicalTime, the former being taken from the simulation
    # output, and the latter an optional keyword to this function. Note that (at least some) Enzo SF/feedback prescriptions
    # use a minimum dynamical time and this parameter is available in the pf, however we offer the user the freedom to 
    # use a different minimum here.
    adjustedDynamicalTime = np.max(np.vstack([np.ones(np.shape(dynamicalTime))*minDynamicalTime, dynamicalTime]),0)
    
    # If we haven't been given a list of times, pick three times near the creation of each particle.
    if times is None:
        times = []
        npts = 3
        for i,time in enumerate(creationTime):
            times.append(time)
            for k in range(npts):
                times.append(time + adjustedDynamicalTime[i]*float(k+1)/npts)
    times = np.array(times)
    times = np.sort(times)
    sfrs = np.zeros(np.shape(times))
    mass = pf['StarMakerMinimumMass'] # May not be consistent with assumptions made in your simulation!
    for i,t in enumerate(times):
        x = (t-creationTime)/adjustedDynamicalTime
        Kx = kernel(x)
        sfrs[i] += np.sum(Kx*mass/adjustedDynamicalTime)
    return times,sfrs


if __name__ == '__main__':
    # Example usage:
    pf=load('/pfs/jforbes/run-enzo-dev-jforbes/dwarf_nf31/DD0185/DD0185')
    dd=pf.h.all_data()
    starParticles = dd["creation_time"] > 0
    mustRefineParticles = dd["particle_type"] == 4
    times,sfrs = sfrFromParticles(pf, dd, mustRefineParticles)

    fig,ax=plt.subplots(figsize=(8,8))
    ax.plot(times*1.0e-6,sfrs,color='b')
    ax.set_xlabel('Time (Myr)')
    ax.set_ylabel('SFR (Msun/yr)')
    ax.set_ylim(0,np.max(sfrs)*1.1)
    plt.savefig('sfr.png')

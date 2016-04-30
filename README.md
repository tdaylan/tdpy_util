This project contains some of my numerical analysis and visualization routines. The primary function is a general purpose MCMC sampler with adaptive burn-in.

### MCMC sampler
The routine `mcmc` is a light-weight MCMC sampler that I use in my research. Given a likelihood function and prior distribution in the parameter space of interest, it takes heavy-tailed Gaussian steps to construct a Markov chain of states, whose stationary distribution is the target probability density. The sampler takes steps in a transformed parameter space where the prior density is uniform. By setting the keyword `optiprop=True`, the sampler takes its initial steps while optimizing its proposal scale until the acceptance ratio is ~ 25%. These samples are later discarded along with the first `numbburn` samples. The chain can also be thinned down by a factor of `factthin`. 

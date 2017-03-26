import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from matplotlib import collections  as mc


def t(alpha, dof):
	# get Student's t value
	return scipy.stats.t.ppf(1-(alpha/2), dof)


def population(pop_mean, n_samples):
	
	# generate population samples
	pop_std  = 2
	return np.random.normal(pop_mean, pop_std, n_samples)


def confidence_interval(sample):

	# compute 90% confidence intervals
	n = len(sample)
	alpha = (1 - 0.90)
	dof = n - 1
	t_crit = t(alpha, dof)
	
	ci = (np.mean(sample) - t_crit*np.std(sample) / np.sqrt(n),
      		np.mean(sample) + t_crit*np.std(sample) / np.sqrt(n))
	
	return ci


def in_ci(true_mean, ci):	
	# is the mean in the CI?
	return (true_mean > ci[0]) & (true_mean < ci[1]) 


def plot_cis(n_trials):
	# plot results
	n = 50
	true_mean = 2
	
	points = []
	ci_bounds = []
	for i in range(n_trials):	

		sample = population(true_mean, n)
		ci = confidence_interval(sample)
		points.append([(i, ci[0]), (i, ci[1])])

		ci_bounds.append(in_ci(true_mean, ci))

	print('The {:0.2f}% of confidence intervals overlap the mean'.format(
		100*(sum(ci_bounds))/n_trials))
		
	c = ['b' if i else 'r' for i in ci_bounds]	

	lc = mc.LineCollection(points, colors=c, linewidths=2)
	fig, ax = plt.subplots()
	plt.axhline(true_mean, color='k')
	ax.add_collection(lc)
	ax.autoscale()
	ax.margins(0.1)
	plt.xticks([])
	plt.savefig('confidence_intervals.png')


if __name__ == '__main__':

	plot_cis(100)


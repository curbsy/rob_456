#ROB456 HW0
#Makenzie Brian
#Import libs
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(0)

#Step 1: create a polynomial
def f_x(x_in):
	c = np.array([-0.1,4.0,-0.1,10.0], float)
	p = np.polyval(c, x_in)
	return p
	
#Plot formatting
def plot_format(axh, xlim=None, title='', xlabel='x', ylabel='f(x)'):
	if xlim is not None:
		axh.set_xlim(xlim)
	axh.set_title(title)
	axh.set_xlabel(xlabel)
	axh.set_ylabel(ylabel)
	

#Main
#Step 2: plot the polynomial
xlim = [-10.0, 25.0]
x = np.linspace(xlim[0], xlim[1], 351, float)
y = f_x(x)
fh1, axh1 = plt.subplots()
axh1.plot(x, y, 'b-')
#axh1.set_xlim(xlim)
#axh1.set_title('Original Polynomial')
#axh1.set_xlabel('x')
#axh1.set_ylabel('f(x)')
plot_format(axh1, xlim, 'Original Polynomial')
fh1.savefig('hw0_original_polynomial.pdf',
bbox_inches='tight')

#Step 3: Chop up polynomial into 14 discrete bins
b_width = (xlim[1]-xlim[0])/14.0
x_bin = np.arange(xlim[0], xlim[1], b_width, float)
y_bin = f_x(x_bin)
fh2, axh2 = plt.subplots()
axh2.bar(x_bin, y_bin, width=b_width, edgecolor='k')  #+b_width/2.0??
#axh1.set_xlim(xlim)
#axh1.set_title('Discreized Bins')
#axh1.set_xlabel('x')
#axh1.set_ylabel('f(x)')
plot_format(axh2, xlim, 'Discretized Bins')
fh2.savefig('hw0_discretized_bins.pdf',
bbox_inches='tight')

#Step 4: Turn intp pdf by normalizing
y_bin_norm = y_bin / y_bin.sum()
fh3, axh3 = plt.subplots()
axh3.bar(x_bin, y_bin_norm, width=b_width, edgecolor='k')  #+b_width/2.0??
plot_format(axh3, xlim, 'Discretized Bins (Normalized), sum = %s' %(y_bin_norm.sum()), ylabel = 'p(x)')
fh3.savefig('hw0_discretized_bins_normalized.pdf',
bbox_inches='tight')

#Step 5: take 500 samples from pdf
#Step 5.1: use random.random(500) to generate 500 samples from uniform random dist
n_samples = 500
x_rand = np.arange(1, n_samples+1, 1, int)
y_rand = np.random.random(n_samples)
fh4, axh4 = plt.subplots()
axh4.plot(x_rand, y_rand, 'k+')
plot_format(axh4, [1, n_samples], '%s samples, uniformly distributed' %n_samples)
fh4.savefig('hw0_%s_uniform_random.pdf' %n_samples, bbox_inches = 'tight')

#Step 5.2: (INCORRECT) shift points to lie between [-10, 25]
y_rand_scaled = y_rand *(xlim[1] - xlim[0]) + xlim[0]
fh5, axh5 = plt.subplots()
axh5.plot(x_rand, y_rand_scaled, 'k+')

#plot bin ranges
for i in range(0, len(x_bin)):
	axh5.plot([1, n_samples], [x_bin[i], x_bin[i]])

plot_format(axh5, [1, n_samples], 'Random samples mapped to x ranges of bins')
fh5.savefig('hw0_random_to_bin_ranges.pdf', bbox_inches = 'tight')

#Step 5.3: (INCORRECT)
y_count_incorrect = np.zeros(x_bin.shape)
for i in range(0, len(y_rand_scaled)):
	for j in range(len(x_bin), 0, -1):
		if y_rand_scaled[i] > x_bin[j-1]:
			y_count_incorrect[j-1] += 1
			break
fh6, axh6 = plt.subplots()			
axh6.bar(x_bin, y_count_incorrect, width=b_width, edgecolor='k')  #+b_width/2.0??
plot_format(axh6, xlim, 'Samples per bin (incorrect)', ylabel = 'samples')
fh6.savefig('hw0_samples_per_bin_incorrect.pdf',
bbox_inches='tight')


#Step 5.2: (CORRECT) leave the samples lying between 0 and 1
#Step 5.3: (CORRECT) use the cdf to divide up the space
y_bin_cdf = y_bin_norm.copy()
i=0
while i < len(y_bin_cdf) - 1:
	i += 1
	y_bin_cdf[i] += y_bin_cdf[i-1]
	
fh7, axh7 = plt.subplots()
axh7.plot(x_rand, y_rand, 'k+')

for i in range(0, len(y_bin_cdf)):
	axh7.plot([1, n_samples], [y_bin_cdf[i], y_bin_cdf[i]])

axh7.set_title('Divindng up the samples according to bin height')
fh7.savefig('hw0_samples_according to bin height.pdf',
bbox_inches='tight')

y_count_correct = np.zeros(x_bin.shape)
for i in range(0, len(y_rand)):
	for j in range(0, len(y_bin_cdf)):
		if y_rand[i] < y_bin_cdf[j]:
			y_count_correct[j] += 1
			break
			
fh8, axh8 = plt.subplots()
axh8.bar(x_bin, y_count_correct, width=b_width, edgecolor='k')  #+b_width/2.0??
plot_format(axh8, xlim, 'Samples per bin (correct)', ylabel = 'samples')
fh8.savefig('hw0_samples_per_bin_correct.pdf',
bbox_inches='tight')



#PART II
x = np.linspace(xlim[0], xlim[1], 351, float)
y = f_x(x)

# Normalize original polynomial plot
p_area = y.sum() * (x[1]-x[0])
y_norm = y/p_area

# Create a figure handle to contain subplots
fh10 = plt.figure(figsize=(12, 4))

#Step 1: Generate 500 uniformly distributed samples in the range 0 to 1 as you did in Step 5.1 above. This time, for each sample, store two numbers - an x value (found by shifting the sample to lie in [-10,25], as in 5.2 above) and a y value (found by evaluating the polynomial at x). Normalize the polynomial (and the samples) as in Step 6 above.
n_samples = 500
s_rand = np.zeros([n_samples, 2])
s_rand[:, 0] = np.random.random(n_samples)
s_rand[:, 0] = s_rand[:, 0] * (xlim[1] - xlim[0]) + xlim[0]
s_rand[:, 1] = f_x(s_rand[:, 0])/p_area

axh10 = fh10.add_subplot(131)
axh10.plot(x, y_norm, 'b-')
axh10.plot(s_rand[:, 0], s_rand[:, 1], 'k+', label='Samples')
plot_format(axh10, title='Normalized polynomial with samples', ylabel='p(x)')
axh10.legend(prop={'size': 6})

fh10.savefig('hw0_normalized_polynomial_with_samples.pdf', bbox_inches='tight')

#Step 2
#What is with the weird squiggle and why does mine center differently???

y_rand_norm = s_rand[:, 1].copy()

i=0
while i < len(y_rand_norm) - 1:
	i += 1
	y_rand_norm[i] += y_rand_norm[i-1]

fh11, axh11 = plt.subplots()
y_rand_norm /= y_rand_norm[len(y_rand_norm)-1]

for i in range(0, len(y_rand_norm)):
	axh11.plot([1, n_samples], [y_rand_norm[i], y_rand_norm[i]])

plot_format(axh11, title='Unsorted Cumulative swatches')

fh11.savefig('hw0_unsorted_cumulative_swatches.pdf', bbox_inches='tight')

#Step 3
n_samp = 5000
s_rand_a = np.random.random(n_samp)
#determine which bin and assign x val of old sample with that bin number
y_counts = np.zeros(y_rand_norm.shape)
for i in range(0, len(s_rand_a)):
	for j in range(0, len(y_rand_norm)):
		if s_rand_a[i] < y_rand_norm[j]:
			y_counts[j] += 1
			break

#normalized by max assigned to bin
#y_counts /= y_counts[len(y_counts)-1]

fh12, axh12 = plt.subplots()
axh12.plot(s_rand[:,0], y_counts, 'b*', label='Density')
#axh12.plot(s_rand[:, 0], s_rand[:, 1], 'k+', label='Weighted Samples from PDF')
plot_format(axh12, title='Density sampling', ylabel='p(x)')
axh12.legend(prop={'size': 6})

fh12.savefig('hw0_density_sampling.pdf', bbox_inches='tight')

plt.show()



import pstats

p = pstats.Stats('test_results/profile')
p.sort_stats('tottime').print_stats(30)
#p.sort_stats('ncalls').print_stats(100)

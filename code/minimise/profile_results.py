import pstats

p = pstats.Stats('profiling/profile_0_0_3')
p.sort_stats('tottime').print_stats(30)
#p.sort_stats('ncalls').print_stats(100)

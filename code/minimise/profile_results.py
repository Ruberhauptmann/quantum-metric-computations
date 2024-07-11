import pstats

p = pstats.Stats('profiling/profile_0_0_4')
p.sort_stats('tottime').print_stats(20)
#p.sort_stats('ncalls').print_stats(100)

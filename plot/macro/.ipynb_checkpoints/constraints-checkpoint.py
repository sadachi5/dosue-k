import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc

rc('text', usetex=True)

HPDM_by_shugo_energy, HPDM_by_shugo_couple = np.loadtxt("../constraints_copy/HPDM_by_shugo.txt", delimiter = ",", unpack = True)
HPDM_by_shugo_energy = HPDM_by_shugo_energy.tolist()
HPDM_by_shugo_couple = HPDM_by_shugo_couple.tolist()
HPDM_by_shugo_energy = [10**n for n in HPDM_by_shugo_energy]
HPDM_by_shugo_couple = [10**n for n in HPDM_by_shugo_couple]
plt.plot(HPDM_by_shugo_energy, HPDM_by_shugo_couple, label = "Cosmological Limit", color="c")
HPDM_by_shugo_upper = [10**-4] * len(HPDM_by_shugo_energy)
plt.plot(HPDM_by_shugo_energy, HPDM_by_shugo_upper, color="c")
plt.fill_between(HPDM_by_shugo_energy, HPDM_by_shugo_couple, HPDM_by_shugo_upper, color="c", alpha=0.2)

Redo_rev_energy, Redo_rev_couple = np.loadtxt("../constraints_copy/Redo_rev.txt", delimiter = ",", unpack = True)
Redo_rev_energy = Redo_rev_energy.tolist()
Redo_rev_couple = Redo_rev_couple.tolist()
Redo_rev_energy = [10**n for n in Redo_rev_energy]
Redo_rev_couple = [10**n for n in Redo_rev_couple]
plt.plot(Redo_rev_energy, Redo_rev_couple, label = "Solar Lifetime", color="g")
Redo_rev_upper = [10**-4] * len(Redo_rev_energy)
plt.plot(Redo_rev_energy, Redo_rev_upper, color="g")
plt.fill_between(Redo_rev_energy, Redo_rev_couple, Redo_rev_upper, color="g", alpha=0.2)

Haloscope_blue_0_energy, Haloscope_blue_0_couple = np.loadtxt("../constraints_copy/Haloscope_blue_0.txt", delimiter = ",", unpack = True)
Haloscope_blue_0_energy = Haloscope_blue_0_energy.tolist()
Haloscope_blue_0_couple = Haloscope_blue_0_couple.tolist()
Haloscope_blue_0_energy = [10**n for n in Haloscope_blue_0_energy]
Haloscope_blue_0_couple = [10**n for n in Haloscope_blue_0_couple]
plt.plot(Haloscope_blue_0_energy, Haloscope_blue_0_couple, label = "Haloscope", color="b")
Haloscope_blue_0_upper = [10**-4] * len(Haloscope_blue_0_energy)
plt.plot(Haloscope_blue_0_energy, Haloscope_blue_0_upper, color="b")
plt.fill_between(Haloscope_blue_0_energy, Haloscope_blue_0_couple, Haloscope_blue_0_upper, color="b", alpha=0.4)

Haloscope_blue_1_energy, Haloscope_blue_1_couple = np.loadtxt("../constraints_copy/Haloscope_blue_1.txt", delimiter = ",", unpack = True)
Haloscope_blue_1_energy = Haloscope_blue_1_energy.tolist()
Haloscope_blue_1_couple = Haloscope_blue_1_couple.tolist()
Haloscope_blue_1_energy = [10**n for n in Haloscope_blue_1_energy]
Haloscope_blue_1_couple = [10**n for n in Haloscope_blue_1_couple]
plt.plot(Haloscope_blue_1_energy, Haloscope_blue_1_couple, color="b")
Haloscope_blue_1_upper = [10**-4] * len(Haloscope_blue_1_energy)
plt.plot(Haloscope_blue_1_energy, Haloscope_blue_1_upper, color="b")
plt.fill_between(Haloscope_blue_1_energy, Haloscope_blue_1_couple, Haloscope_blue_1_upper, color="b", alpha=0.4)

Haloscope_blue_2_energy, Haloscope_blue_2_couple = np.loadtxt("../constraints_copy/Haloscope_blue_2.txt", delimiter = ",", unpack = True)
Haloscope_blue_2_energy = Haloscope_blue_2_energy.tolist()
Haloscope_blue_2_couple = Haloscope_blue_2_couple.tolist()
Haloscope_blue_2_energy = [10**n for n in Haloscope_blue_2_energy]
Haloscope_blue_2_couple = [10**n for n in Haloscope_blue_2_couple]
plt.plot(Haloscope_blue_2_energy, Haloscope_blue_2_couple, color="b")
Haloscope_blue_2_upper = [10**-4] * len(Haloscope_blue_2_energy)
plt.plot(Haloscope_blue_2_energy, Haloscope_blue_2_upper, color="b")
plt.fill_between(Haloscope_blue_2_energy, Haloscope_blue_2_couple, Haloscope_blue_2_upper, color="b", alpha=0.4)

suzuki_hpdm_energy, suzuki_hpdm_couple = np.loadtxt("../constraints_copy/suzuki_hpdm.txt", delimiter = ",", unpack = True)
suzuki_hpdm_energy = suzuki_hpdm_energy.tolist()
suzuki_hpdm_couple = suzuki_hpdm_couple.tolist()
suzuki_hpdm_energy = [10**n for n in suzuki_hpdm_energy]
suzuki_hpdm_couple = [10**n for n in suzuki_hpdm_couple]
#plt.plot(suzuki_hpdm_energy, suzuki_hpdm_couple, label = "Suzuki et al.", color="g")
suzuki_hpdm_upper = [10**-4] * len(suzuki_hpdm_energy)
#plt.plot(suzuki_hpdm_energy, suzuki_hpdm_upper, color="g")
#plt.fill_between(suzuki_hpdm_energy, suzuki_hpdm_couple, suzuki_hpdm_upper, color="g", alpha=0.4)

result_raw_energy, result_raw_couple = np.loadtxt("../constraints_copy/result_raw.txt", unpack = True)
result_raw_energy = result_raw_energy.tolist()
result_raw_couple = result_raw_couple.tolist()
result_raw_energy = [n*(10**-6) for n in result_raw_energy]
result_raw_couple = [n for n in result_raw_couple]
plt.plot(result_raw_energy, result_raw_couple, label = "Previous experiment", color="k")
result_raw_upper = [10**-4] * len(result_raw_energy)
plt.plot(result_raw_energy, result_raw_upper, color="k")
plt.fill_between(result_raw_energy, result_raw_couple, result_raw_upper, color="k", alpha=1)

ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')
plt.xlim(10 ** -6, 10 ** -1)
plt.ylim(10 ** -11, 10 ** -8)
plt.xlabel("dark photon mass " + "$m_\gamma$" + "[eV]", fontsize = 13)
plt.ylabel("mixing parameter " + "$\chi$", fontsize = 13)
plt.title("constraints", fontsize = 15)

plt.tick_params(labelsize=13)
plt.tight_layout()

#plt.legend()
plt.savefig("../figure/constraintsTest.pdf")
#plt.show()

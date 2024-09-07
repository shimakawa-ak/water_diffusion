# chargeはただの電荷数，LJは↓を参照
# https://pubs.acs.org/doi/10.1021/jp8001614

# %%
import sys, os
from myradonpy.func import base

n_cpu = 32 # Number of CPU cores
# n_cpu = radonpy.core.utils.cpu_count() # Number of CPU cores
n_memory = 1000*64 # Memory in MB
temp = 300
press = 1.0
use_mpi = True
rate = 1.0 # 割合
efield_kVmm = 0 # kV/mm

name = 'PPG_TPA_test' # 保存先の名前
smiles = '*OC(C)C*' # SMILES
smi_add = "O=C=NCCCCCCn1c(=O)n(CCCCCCN=C=O)c(=O)n(CCCCCCN=C=O)c1=O"
n_add = 2*5 #OH数に合わせて偶数が良い
rate_NCO_OH = 1
n_oligomer = rate_NCO_OH*(n_add*3)//2
smi_ter1 = "*C(=O)/C=C(C)\\NCCO"
smi_ter2 = "*OC(=O)/C=C(C)\\NCCO"
natom_oligomer = 60
# 主剤の繰り返し単位はn=5,6、原子数は12*5=60
# オリゴマー全体の分子量は600-650、原子数は100か
# 72*n_add+100*n_oligomer = 2220 (n_add = 2*5)

n_sep = 1 # 並列数
dir_base = '../result'
work_dir = f'{dir_base}/{name}'
os.makedirs(work_dir, exist_ok=True)

cpu = int(n_cpu/n_sep)
memory = int(n_memory/n_sep)
mpi_cpu = cpu if use_mpi else -1

print(f"name:{name}, smiles:{smiles}, work_dir:{work_dir}, ff:GAFF2, n_sep:{n_sep}, cpu:{cpu}, memory:{memory}, use_mpi:{use_mpi}, n_oligomer:{n_oligomer}, n_add:{n_add}\n")

# %%
# d_rate変更時はonly_side=Trueになっている点に注意
random_seed = 0
system = base.MakeSystemEQ(work_dir, mpi_cpu, memory, smiles, smi_add=smi_add, n_add=n_add, load_cell=True, natom_oligomer=natom_oligomer, n_oligomer=n_oligomer, natom_qm=20, qm_calc=False, temp=temp, press=press, random_seed=random_seed, ter1=smi_ter1, ter2=smi_ter2)
cell_with_ion = system.make_system_and_run_eq_with_check_restore(eq_step=1.0,)

# %%
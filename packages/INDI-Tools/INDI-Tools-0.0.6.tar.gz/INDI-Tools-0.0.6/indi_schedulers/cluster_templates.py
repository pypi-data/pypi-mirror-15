# indi_schedulers/cluster_templates.py
#

# Make directory
mkdir_str = 'mkdir -p %(job_folder)s'

# Start task ID string
start_taskid_str = 'echo "Start - TASKID " %(env_arr_idx)s " : " $(date)'

# End task ID string
end_taskid_str = 'echo "End - TASKID " %(env_arr_idx)s " : " $(date)'

# SGE template string
pbs_template = \
'''#! %(shell)s
## PBS batch file - %(timestamp)s
#PBS -S %(shell)s
#PBS -N %(job_name)s
#PBS -t 1-%(num_tasks)d
#PBS -q %(queue)s
#PBS -l nodes=1:ppn=%(cores_per_task)d
#PBS -A %(user)s
#PBS -V
#PBS -wd %(work_dir)s
'''
# Add in start, run_cmd, end
pbs_template = '\n'.join([pbs_template,
                          start_taskid_str, '%(run_cmd)s', end_taskid_str])

# SGE template string
sge_template = \
'''#! %(shell)s
## SGE batch file - %(timestamp)s
#$ -S %(shell)s
#$ -N %(job_name)s
#$ -t 1-%(num_tasks)d
#$ -q %(queue)s
#$ -pe %(par_env)s %(cores_per_task)d
#$ -A %(user)s
#$ -V
#$ -wd %(work_dir)s
'''
# Add in start, run_cmd, end
sge_template = '\n'.join([sge_template,
                          start_taskid_str, '%(run_cmd)s', end_taskid_str])

# SLURM template string
slurm_template = \
'''#! %(shell)s
## SLURM batch file - %(timestamp)s
#SBATCH --job-name=%(job_name)s
#SBATCH --array=1-%(num_tasks)d
#SBATCH --cpus-per-task=%(cores_per_task)d
#SBATCH --uid=%(user)s
#SBATCH --get-user-env
#SBATCH --workdir=%(work_dir)s
#SBATCH --time=%(time_limit)s
'''
# Add in start, run_cmd, end
slurm_template = '\n'.join([slurm_template,
                            start_taskid_str, '%(run_cmd)s', end_taskid_str])

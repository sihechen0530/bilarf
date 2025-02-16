module load cuda/11.8
conda activate bilarf_310
export CC=$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-gcc
export CXX=$CONDA_PREFIX/bin/x86_64-conda-linux-gnu-g++ 
$CC --version

# pip install ./gridencoder
# pip install --no-build-isolation --no-binary :all: ./gridencoder

export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:/shared/centos7/cuda/11.8/lib64:/shared/centos7/nodejs/14.15.4/lib:/shared/centos7/anaconda3/2022.05/lib:$LD_LIBRARY_PATH

# CUDA=cu118
# pip install torch-scatter -f https://data.pyg.org/whl/ torch-2.0.0+${CUDA}.html

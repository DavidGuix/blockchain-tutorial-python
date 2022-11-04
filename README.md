# Blockchain Tutorial with Python

In this tutorial you will learn the basic notions and knowledge about the Blockchain technology as well as some practical examples about retrieving and visualizing data from a blockchain via public APIs with Python.

We will focus mostly on the [Ethereum](https://ethereum.org) blockchain.

For any comments about the tutorial (suggestions for improvement, typos, error reports, etc) you can [open an Issue](https://github.com/dsalgador/blockchain-tutorial-python/issues/new) or create a  [Pull Request](https://github.com/dsalgador/blockchain-tutorial-python/pulls). You can also contact me at `daniel.salgado.rojo@gmail.com`.

Before start working with the tutorial notebook(s), please follow the steps in the [prerequisites & setup section](#prerequisites--setup).


After you complete sections 1, 2 and 3, I recommend you doing the proposed Exercises. You can fork this repository and work locally in your forked repo.

The reader is encouraged to provide its solutions to usecases it they are still not present in the `usecases/` directory via a pull request. Read the [usecase solutions guidelines section](#contributing-with-use-cases-requirements-and-guidelines) for more details about how to do it.


## Prerequisites & Setup

1. To execute the code in Section 3, you will need to fill the `api_keys.json` file with your own API keys, as you will see when you follow the tutorial.

2. Install a Python environment with the modules listed in the `requirements.txt`. You may need to install `jupyter notebook` too. If you can use `conda`, follow the steps below:

    ### Environment setup with 'conda' (Tested in Ubuntu 20.04)

    * Step 1. Create conda environment from environment.yml file. From the terminal in the project folder run
        ``` 
        conda env create -f environment.yml
        ```
        Now by running 
        ```
        conda env list
        ```
        the environment `blockchain_tutorial_python` should be seen.

    * Step 2. Activate the environment
        ```
        conda activate blockchain_tutorial_python
        ```

    * Step 3. Create a jupyter notebook kernel using the environment:
        ```
        (blockchain_tutorial_python) ipython kernel install --user --name=blockchain_tutorial_python --display-name "BlockchainTutorial (Conda py3.9)"
        ```

    * Step 4. Open jupyter and use the available notebooks if desired:
        ```
        (blockchain_tutorial_python) jupyter notebook
        ```

        If you where already using jupyter, refreshing one of the notebooks if necessary and going to Kernel --> Change kernel, we should see a "BlockchainTutorial (Conda py3.9)" kernel that we can select.

If at some point more modules are added to the requirements files, you can update the conda environment you already created with the following command:

```bash
conda env update --name blockchain_tutorial_python --file environment.yml --prune
```

If you are facing issues with creating a conda environment and a Jupyer kernel with it, you could just install all the required modules in your "main" (base) Python from a terminal using `"pip install"`  commands.


## Contributing with Use cases: Requirements and guidelines


0. Learn about basic contributing steps [here](https://gist.github.com/MarcDiethelm/7303312) (fork the repository, create a new branch....).
1. Create a new subfolder inside the `usecases/` folder that is at the same level as the `src/` folder. The name of the subfolder should be representative for the use case you provide, lets call it `<A short folder name for your usecase>`.
2. Create a new jupyter notebook inside the subfolder created in step 1.

- Additional core code used outside of the notebook, should be located at `src/usecases/<A short folder name for your usecase>`
- Structure the Jupyter cells of your use case solution alternating markdown (for explanations, background, etc) cells and code cells. Add some interpretable plots.
- All code put in the src/ directory should pass code-quality tests. It is compulsory to pass the "tox" command, which tests the code with `pylint` and `mypy`. We are using the `typing` Python's module to type functions and classes.


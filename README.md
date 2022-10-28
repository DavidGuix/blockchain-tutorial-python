# Blockchain Tutorial with Python

In this tutorial you will learn the basic notions and knowledge about the Blockchain technology as well as some practical examples about retrieving and visualizing data from a blockchain via public APIs with Python.

We will focus mostly on the [Ethereum](https://ethereum.org) blockchain.

For any comments about the tutorial (suggestions for improvement, typos, error reports, etc) you can [open an Issue](https://github.com/dsalgador/blockchain-tutorial-python/issues/new) or create a  [Pull Request](https://github.com/dsalgador/blockchain-tutorial-python/pulls). You can also contact me at `daniel.salgado.rojo@gmail.com`.

After you complete sections 1, 2 and 3, I recommend you doing the proposed Exercises. You can fork this repository and work locally in your forked repo,


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

If you are facing issues with creating a conda environment and a Jupyer kernel with it, you could just install all the required modules in your "main" (base) Python from a terminal using `"pip install"`  commands.
# Getting Started

## Installation

consumo is a Python project. That means you have two main Python related ways to get it.

Option A: Via Python

:   If you have Python (⋝ 3.12) installed, you can use it to install consumo. From your terminal, run:

    ```shell
    python -m pip install consumo
    # python3 -m pip3 install consumo
    ```

Option B: Standalone Binaries

:   If you're on a MacOS or Windows system and don't want to deal with Python, bundled binaries are available.

    1. Go to the project's [Releases](https://github.com/gbr-ufs/consumo/releases/latest) page.
    2. Install the appropriate binary for your operating system.
    3. Place it in a directory that's in your system's PATH.
    4. Enjoy!

Option C: System Package

:   Linux users can install consumo from the comfort of their favorite package manager. Just check if your package manager or distro is under here:

    [![packaging status](https://repology.org/badge/vertical-allrepos/consumo.svg)](https://repology.org/project/consumo/versions)

## Your First Calculation

Let's try consumo out by figuring out how long it takes to read a single webpage.

Open your terminal and run the `consumo url` command. It takes a link (or multiple links!) as its argument:

```shell
consumo url https://example.com
```

consumo will then analyze the contents of the page and return the estimated reading time based on the standard reading speed.

Let's see how it does with files. From your terminal, write the following commands to create a simple "Hello, World!" file:

```shell
echo "Hello, World!" > hello_world.txt
```

Now, let's throw consumo at it:

```shell
consumo file hello_world.txt
```

consumo also has a third parameter, `list`, that allows us to calculate the consumption time of a text file full of links:

```shell
echo "https://example.com" > links.txt
echo "https://example.org" >> links.txt
```

```shell
consumo list links.txt
```

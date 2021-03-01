# GenericMultiTaskingExecuter

GenericMultiTaskingExecuter is a framework which allows you to run, in parallel, logical units of work which can be modeled as graph of tasks that contains depedencies between tasks, in the sense that one task is run only after its depended tasks have finished their run.

The uniqueness of this framework is that it can "ride" 




# Prerequisites
The code is compatible with python 3.7 version.





<!--- If you use this project in your work please cite: 
If you use this project in your work please cite: 
> "AAAAA",  
>
> Bornstein, Asa and Hendler, Danny and Rubin, Amir,
>
> 3rd International Winter School and Conference on Network Science, 2017.--->


# Example
For a simple execution on a dummy input, cd to stable:
```sh
$ cd Stable
```
and run:
```sh
$ java -jar NECTAR.1.0.jar Dummy
```
(Same as running:)
```sh
$ java -jar NECTAR.1.0.jar ./lib/DummyNet.txt ./DummyOutput
```

# What's in this repo?

## Stable
Under 'Stable' you will find the latest version. Note - it does not support threads.


## Tools

Under 'Tools' you can find our implementation to the Omega-Index and Average F1 score calculating tool. 

Under 'Tools/ML' you can find the training set used to train the Random Forst used by NECTAR.

## Older versions
Under 'Versions' you will find old various versions of NECTAR, supporting threads and weighted graphs. 

We will not continue to devolop them.

For instance, under 'V1' you can find two java implemented version to the NECTAR algorithm (one with modularity, one with WOCC).

('V2' is the version similar to 'V1', except that the objective function is chosen by the algorithm.)













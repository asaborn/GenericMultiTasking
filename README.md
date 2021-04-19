# GenericMultiTaskingExecuter

GenericMultiTaskingExecuter is a framework which allows you to define logical units of work and also dependencies between them, in the sense that a depended logical unit must follow the completion of another. This forms a dependencies graph of tasks which determines which of the tasks can run in parallel or sequential mode (if one is dependent of another).

This definition is implementation independent to which hardware and software architecture will be used for the parallel run of those tasks. As a result, the framework provides the ability to run those tasks over different parallel computing architectures and also to add more architectures implementations in the future.

## Currently supported parallel computing architectures

Oracle Grid Engine - Distributed computing

Slurm Workload Manager - Distributed computing

Taskgraph - https://github.com/natcap/taskgraph

## Tasks grouping 

Each task has a 'group' attribute which defines to which group it belongs to. Usually, grouped tasks are depended of each other and must run in a sequential mode. Tagging the tasks to a group, in practice, enforces their sequential run to be executed on the same hardware core. For example, it parallelism is achieved using distributed computing architecture, this will ensure that all grouped tasks will run sequentially on the same computer under the same job.

# Prerequisites
The code is compatible with python 3.7 version.

## Logical unit of work parameters

Each logical unit of work is basically running an executable with the command line paramaters.
```

OutputDirectory			[The run outputs will be located at this path]
CmdLine				[The command line which runs the task in the shell]
BinariesLocation		[The folder of the binary files which run]
Force				[Force run even though outputs are exist in output directory (outputs will be overwritten]
StdoutFile			[Path to the stdout file]
StderrFile			[Path to the stderr file]
TimeoutInSecs			[Timeout in seconds for the runtime. If exceeds runtime, the logical unit is terminated]
GeneratedFiles			[Files names of the generated files. Used for the 'Force' flag]
CheckInputFilesBeforeRun	[Check if input files exists in paths. If not exist, the logical unit won't run]
WorkingDirectoryToBinariesDir	[Flag which indicates whether the working directory is set to the binaries folder]
MaxMemoryUsage			[Maximum memory usage. Used in architectures where this should be declared before run]
ExecutionTimeFile		[Path to the execution time file which stores the total execution time of the logical unit]

```


<!--- If you use this project in your work please cite: 
If you use this project in your work please cite: 
> "Machine-Learning Based Objective Function Selection for Community Detection ",  
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













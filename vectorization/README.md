### Vectorization

This module aims to generate embeddings from the text of any html pages of interest and create [Faiss vector database](https://faiss.ai/) file.

Vectorization can be time consuming depending on the content to vectorize and the available compute that can be leveraged. In this particular case, it is being run as an Azure ML job. 

**Pre-requisite** to running this job is creation of workspace, environment, and compute cluster in Azure ML. 

[aml_job.yml](aml_job.yml) contains the job configuration details and following are the salient parameters:

1. **```command```**- encompasses what code to trigger. The input is html files and they are kept in datastore ```azureml://datastores/workspaceblobstore/paths/__input_folder__```, where ```__input_folder__``` is the place holder to be replaced with appropriate folder path. By default, Azure ML creates ```workspaceblobstore``` for every workspace and the same can be leveraged. Similarly, the vector DB files will be created in ```azureml://datastores/workspaceblobstore/paths/__output_folder__```, where ```__output_folder__``` is a place holder to which ```index.faiss``` and ```index.pkl``` files are written to  

2. **```environment```** - Azure ML environment in which the code will be executed. Environment refers to docker image and in this case it is ubuntu base image with python packages as mentioned in [conda_env.yml](conda_env.yml) are installed. Refer [aml_env.yaml](aml_env.yaml)

3. **```compute```** - Compute nodes on which docker containers, created from environment, will be run. There are various compute types offered by Azure ML, but in this case we rely on compute cluster. Refer [aml_compute.yml](aml_compute.yml)


**Note**: Each yml file has comments with Azure cli commands to use and reference links

#### Sequence of steps for reference

**Pre-requisite**: Install and setup [Azure Cli ml extension V2](https://learn.microsoft.com/en-in/azure/machine-learning/how-to-configure-cli?view=azureml-api-2&tabs=public)
```
az account set --subscription <subscription>

az configure --defaults workspace=<workspace> group=<resource-group> location=<location>

az ml environment create --file aml_env.yaml

az ml compute create --file aml_compute.yml

az ml job create --file aml_job.yml
```


### Code

[vectorization.py](vectorization.py) is the main file which gets triggered when the job is run. It actually uses ```ray``` to parallize the vectorization. The environment (docker image) would have ray installed as part of conda_env.yml


To generate embeddings, HuggingFace's sentence-transformer model [multi-qa-mpnet-base-dot-v1](https://huggingface.co/sentence-transformers/multi-qa-mpnet-base-dot-v1) is being leveraged. This seems to generate dense vectors which aid in semantic search for queries, questions etc.
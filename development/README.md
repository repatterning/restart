<br>

<span style="color: #777777"><b>IN PROGRESS</b></span>

<br>

* [Remote & Local Environments](#remote--local-environments)
  * [Remote](#remote) 
  * [Local](#local)
* [GitHub Actions](#github-actions)
  * [Code Analysis](#code-analysis)
  * [Container Registry Packages](#container-registry-packages)
* [Testing Images Containers](#testing-image-containers)
  * [Locally](#locally)
  * [Via Amazon EC2 (Elastic Compute Cloud)](#via-amazon-ec2-elastic-compute-cloud)
* [References](#references)

<br>

## Remote & Local Environments

### Remote

The remote environment's image is built via

```shell
docker build . --file .devcontainer/Dockerfile -t pollutants
```

This names the new image `pollutants`.  Subsequently, a container/instance of the image `pollutants` is set up via:

> docker run [--rm](https://docs.docker.com/engine/reference/commandline/run/#:~:text=a%20container%20exits-,%2D%2Drm,-Automatically%20remove%20the) [-i](https://docs.docker.com/engine/reference/commandline/run/#:~:text=and%20reaps%20processes-,%2D%2Dinteractive,-%2C%20%2Di) [-t](https://docs.docker.com/get-started/02_our_app/#:~:text=Finally%2C%20the-,%2Dt,-flag%20tags%20your) [-p](https://docs.docker.com/engine/reference/commandline/run/#:~:text=%2D%2Dpublish%20%2C-,%2Dp,-Publish%20a%20container%E2%80%99s) 127.0.0.1:10000:8888 -w /app --mount \
> &nbsp; &nbsp; type=bind,src="$(pwd)",target=/app pollutants

Herein, `-p 10000:8888` maps the host port `10000` to container port `8888`.  Note, the container's working environment,
i.e., -w, must be inline with this project's top directory.  Get the name of the running instance ``pollutants`` via:

```shell
docker ps --all
```

A developer may attach an IDE (independent development environment) application to a running container.  The IntelliJ 
IDEA instructions are:

> Connect to the Docker [daemon](https://www.jetbrains.com/help/idea/docker.html#connect_to_docker)
> * **Settings** $\rightarrow$ **Build, Execution, Deployment** $\rightarrow$ **Docker** $\rightarrow$ **WSL:** `operating system`
> * **View** $\rightarrow$ **Tool Window** $\rightarrow$ **Services** <br>Within the **Containers** section connect to the running instance of interest, or ascertain connection to the running instance of interest.

Visual Studio Code has its container attachment instructions; study [Attach Container](https://code.visualstudio.com/docs/devcontainers/attach-container).

<br>

### Local

For temporary explorations via a local environment, first update your machine's base `conda` environment, i.e.,

```shell
conda update -n base -c anaconda conda
```

Subsequently, build a local virtual environment via the command

```shell
conda env create --file environment.yml -p /opt/miniconda3/envs/pollutants
```

Herein, **environment.yml** uses the same **requirements.txt** as [Dockerfile](/.devcontainer/Dockerfile).  If the 
environment exists, i.e., if the aim is to replace an existing environment, initially run

```shell
conda env remove --name pollutants
```

<br>
<br>

## GitHub Actions

<span style="margin-bottom: 25px"><b>Integration, Delivery, Deployment</b></span>

The project uses GitHub Actions for a variety of code analysis, and to automatically deliver images to container registries.

### Code Analysis

Study the code analysis steps outlined in [`.github/workflows/main.yml`](/.github/workflows/main.yml).  The steps therein 
mimic local code analysis steps.  For example, 

```shell
python -m pylint --rcfile .pylintrc ...
```

will analyse a program or set of programs; depending on the ellipsis replacement. Note, the directive below generates the 
dotfile `.pylintrc` of the static code analyser [pylint](https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html).

```shell
pylint --generate-rcfile > .pylintrc
```

<br>

### Container Registry Packages

The **packages** section of [main.yml](/.github/workflows/main.yml) is for GitHub Container Registry (GCR) container 
registration.  Beware of errors due to:


> **Case** _permission denied_ $\rightarrow$ the **packages** section of [main.yml](/.github/workflows/main.yml) is probably 
missing:

```yaml
permissions:
  contents: read
  packages: write
```

> **Case** _the image does not exist locally_ $\rightarrow$ the **packages** section of [main.yml](/.github/workflows/main.yml) is probably
missing:

```yaml
docker build . --file Dockerfile --tag ...
```

<br>

The **ecr** section of [main.yml](/.github/workflows/main.yml) is for Amazon Elastic Container Registry (ECR) container 
registration.

<br>
<br>


## Testing Image Containers

### Locally

The image's programs interact with Amazon services therefore an image container will require Amazon credentials.  Hence, 
a testing option is a `compose.yaml`; a `compose.yaml` of the form [compose.yaml.template](/compose.yaml.template), 
**explanatory notes upcoming**.  Subsequently, within the directory hosting `compose.yaml`

```shell
 docker pull ghcr.io/enqueter/pollutants:develop
 docker compose up -d
```

If any problems arise

```shell
docker compose logs -f
```

<br>

### Via Amazon EC2 (Elastic Compute Cloud)

If the EC2 is launched with the appropriate instance profile policies for interacting with relevant Amazon services, then 
testing is straightforward.

```shell
docker pull ghcr.io/enqueter/pollutants:develop
docker run ghcr.io/enqueter/pollutants:develop
```

<br>
<br>

## References

* [Epoch Time](https://unixtime.org)
* [UNIX Time Converters](https://time.is/Unix_time_converter)
* [Time Durations](https://en.wikipedia.org/wiki/ISO_8601#Durations)
* [ubuntu man pages](https://manpages.ubuntu.com/manpages/trusty/man1/)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>

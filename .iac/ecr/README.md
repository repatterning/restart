<br>

### Notes

The script [registry.sh.template](registry.sh.template) outlines the [creation of an Amazon ECR (Elastic Container Registry) repository](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ecr/create-repository.html).  Always ensure the _**tags text**_, study [registry.json](registry.json), does not include special characters.

```shell
bash .iac/ecr/registry.sh
```

Repository [deletion](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ecr/delete-repository.html):

```shell
aws ecr delete-repository \
    --repository-name {repository.name} \
    --force
```



<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
